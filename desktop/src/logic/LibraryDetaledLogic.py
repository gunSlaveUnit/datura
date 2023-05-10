import gzip
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from enum import Enum, auto
from datetime import datetime, timedelta
from pathlib import Path

import requests
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer, QUrl

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL, BUILDS_URL, PLATFORMS_URL
from server.src.core.utils.io import CHUNK_SIZE


def _check_game_installed(game_id: int) -> bool:
    with open("../app_config.json", "r") as app_config_file:
        config = json.load(app_config_file)
        for app in config["apps"]:
            if game_id == app['game_id']:
                return True
        return False


class LibraryDetailedLogic(QObject):
    class AppStatus(int, Enum):
        NOT_INSTALLED = 0
        INSTALLED = auto()
        LOADING = auto()
        RUNNING = auto()
        NOT_AVAILABLE = auto()

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._id = None
        self._auth_service = auth_service

        self.app = None
        self._app_status = self.AppStatus.NOT_INSTALLED

        self._game_id = -1
        self._game_title = ''
        self._last_launched = ''
        self._play_time = ''

        self._installation_path = ''
        self._loading_progress = ''

        self.time = 0
        self.timer = QTimer()
        minute = 1000 * 60
        self.timer.setInterval(minute)
        self.timer.timeout.connect(self.timer_tick)

    def timer_tick(self):
        minute = 60
        self._auth_service.authorized_session.put(LIBRARY_URL + f'{self._id}/', json={
            "game_time": self.time + minute,
            "last_run": datetime.today().timestamp()
        })
        self.map(self._game_id)

    # region App status

    app_status_changed = Signal()

    @Property(int, notify=app_status_changed)
    def app_status(self):
        return self._app_status

    @app_status.setter
    def app_status(self, new_value: int):
        if self._app_status != new_value:
            self._app_status = new_value
            self.app_status_changed.emit()

    # endregion

    # region Game title

    game_title_changed = Signal()

    @Property(str, notify=game_title_changed)
    def game_title(self):
        return self._game_title

    @game_title.setter
    def game_title(self, new_value: str):
        if self._game_title != new_value:
            self._game_title = new_value
            self.game_title_changed.emit()

    # endregion

    # region Last launched

    last_launched_changed = Signal()

    @Property(str, notify=last_launched_changed)
    def last_launched(self):
        return self._last_launched

    @last_launched.setter
    def last_launched(self, new_value: str):
        if self._last_launched != new_value:
            self._last_launched = new_value
            self.last_launched_changed.emit()

    # endregion

    # region Play time

    play_time_changed = Signal()

    @Property(str, notify=play_time_changed)
    def play_time(self):
        return self._play_time

    @play_time.setter
    def play_time(self, new_value: str):
        if self._play_time != new_value:
            self._play_time = new_value
            self.play_time_changed.emit()

    # endregion

    # region Installation path

    installation_path_changed = Signal()

    @Property(str, notify=installation_path_changed)
    def installation_path(self):
        return self._installation_path

    @installation_path.setter
    def installation_path(self, new_value: str):
        if self._installation_path == new_value:
            return
        self._installation_path = new_value
        self.installation_path_changed.emit()

    # endregion

    # region Loading progress

    loading_progress_changed = Signal()

    @Property(str, notify=loading_progress_changed)
    def loading_progress(self):
        return self._loading_progress

    @loading_progress.setter
    def loading_progress(self, new_value: str):
        if self._loading_progress == new_value:
            return
        self._loading_progress = new_value
        self.loading_progress_changed.emit()

    # endregion

    @Slot(int)
    def map(self, game_id: int):
        current_user_id = self._auth_service.current_user.id
        params = {
            "user_id": current_user_id,
            "game_id": game_id
        }

        response = self._auth_service.authorized_session.get(LIBRARY_URL, params=params)
        if response.ok:
            data = response.json()[0]

            self._id = data["id"]
            self._game_id = data["game"]["id"]
            self.game_title = data["game"]["title"]

            if _check_game_installed(data["game"]["id"]):
                if self.app is not None:
                    self.app_status = self.AppStatus.RUNNING
                else:
                    self.app_status = self.AppStatus.INSTALLED

            self.time = data["game_time"]
            if self.time < 3600:
                self.play_time = f"{self.time // 60} m"
            else:
                self.play_time = f"{self.time / 3600:.1f} h"

            possible_last_launch_stamp: int | None = data["last_run"]
            if possible_last_launch_stamp:
                launch_date = datetime.fromtimestamp(possible_last_launch_stamp)

                if datetime.today().date() == launch_date.date():
                    self.last_launched = "Today"
                elif datetime.today().date() - timedelta(1) == launch_date.date():
                    self.last_launched = "Yesterday"
                else:
                    self.last_launched = launch_date.strftime('%d %b %Y')
            else:
                self.last_launched = "Never"

    def load_build_files(self):
        params = {"game_id": self._game_id}
        builds = requests.get(BUILDS_URL, params=params).json()

        platforms = self._auth_service.authorized_session.get(PLATFORMS_URL).json()

        for build in builds:
            platform_id = build['platform_id']
            platform = next((platform for platform in platforms if platform['id'] == platform_id), None)
            if platform:
                if platform['title'] == sys.platform:
                    get_build_filenames = BUILDS_URL + str(build["id"]) + '/files/'
                    files = requests.get(get_build_filenames).json()['files']

                    processed_bytes = 0
                    build_size_bytes = sum([file['size_bytes'] for file in files])
                    self.loading_progress = 'Downloading ... 0%'

                    app_config_file = open("../app_config.json", "r")
                    config = json.load(app_config_file)
                    app_config_file.close()

                    game_installation_path = Path(config["default_games_installation_path"][sys.platform])
                    if sys.platform == 'linux':
                        game_installation_path = game_installation_path.joinpath(os.getlogin())
                    game_installation_path = game_installation_path.joinpath(config["default_library_path_name"], self.game_title)

                    Path.mkdir(game_installation_path, parents=True)

                    for file in files:
                        file_url = get_build_filenames + f'?filename={file["rel_path"]}'

                        response = requests.get(file_url, stream=True)

                        file_name = game_installation_path.joinpath(file["rel_path"])
                        possible_directory = file_name.parent

                        if not possible_directory.exists():
                            possible_directory.mkdir(parents=True, exist_ok=True)

                        with open(game_installation_path.joinpath(file_name), "wb") as f:
                            with gzip.GzipFile(fileobj=response.raw, mode="rb") as gz:
                                while True:
                                    chunk = gz.read(CHUNK_SIZE)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                                    processed_bytes += len(chunk)
                                    self.loading_progress = f"Downloading ... {(processed_bytes / build_size_bytes * 100):.2f}%"

                    game_running_config = {
                        "game_id": build["game_id"],
                        "path": game_installation_path.name,
                        "call": build["call"]
                    }
                    if build["params"]:
                        game_running_config["params"] = build["params"]

                    config["apps"].append(game_running_config)

                    app_config_file = open("../app_config.json", "w")
                    json.dump(config, app_config_file)
                    app_config_file.close()
                break

    def loading_done(self, task):
        self.app_status = self.AppStatus.INSTALLED

    @Slot()
    def download(self):
        self.app_status = self.AppStatus.LOADING
        executor = ThreadPoolExecutor(1)
        future = executor.submit(self.load_build_files)
        future.add_done_callback(self.loading_done)
        self.loading_progress = 'Grab build ...'

    @Slot()
    def launch(self):
        with open("../app_config.json", "r") as app_config_file:
            config = json.load(app_config_file)
            apps = config["apps"]

            for app in apps:
                if self._game_id == app['game_id']:
                    path = Path(config["default_games_installation_path"][sys.platform])
                    if sys.platform == 'linux':
                        path = path.joinpath(os.getlogin())

                    path = path.joinpath(config["default_library_path_name"], app['path'], app['call'])

                    params = app['params'].split() if 'params' in app else []

                    self.app = subprocess.Popen(path, *params, stdout=subprocess.PIPE)
                    self.app_status = self.AppStatus.RUNNING
                    self.timer.start()
                    self._auth_service.authorized_session.put(LIBRARY_URL + f'{self._id}/', json={
                        "game_time": self.time,
                        "last_run": datetime.today().timestamp()
                    })
                    break

    @Slot()
    def shutdown(self):
        self.app.terminate()
        self.app.kill()
        self.app.wait()
        self.app_status = self.AppStatus.INSTALLED
        self.timer.stop()
