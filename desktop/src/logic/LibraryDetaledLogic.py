import gzip
import json
import signal
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL, BUILDS_URL, PLATFORMS_URL


class LibraryDetailedLogic(QObject):
    game_title_changed = Signal()
    is_game_installed_changed = Signal()
    last_launched_changed = Signal()
    play_time_changed = Signal()
    installation_path_changed = Signal()
    is_running_changed = Signal()

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._id = None
        self._auth_service = auth_service

        self._game_id = -1
        self._game_title = ''
        self._is_game_installed = False
        self._last_launched = False
        self._play_time = ''
        self._installation_path = ''
        self._is_running = False

        self.app = None
        self.timer = QTimer()
        minute = 1000 * 60
        self.timer.setInterval(minute)
        self.timer.timeout.connect(self.timer_callback)

    def timer_callback(self):
        self._auth_service.authorized_session.put(LIBRARY_URL + f'{self._id}/', json={
            "game_time": 1
        })

    # region Game title

    @Property(str, notify=game_title_changed)
    def game_title(self):
        return self._game_title

    @game_title.setter
    def game_title(self, new_value: str):
        if self._game_title != new_value:
            self._game_title = new_value
            self.game_title_changed.emit()

    # endregion

    # region Is game installed

    @Property(bool, notify=is_game_installed_changed)
    def is_game_installed(self):
        return self._is_game_installed

    @is_game_installed.setter
    def is_game_installed(self, new_value: bool):
        if self._is_game_installed != new_value:
            self._is_game_installed = new_value
            self.is_game_installed_changed.emit()

    # endregion

    # region Last launched

    @Property(str, notify=last_launched_changed)
    def last_launched(self):
        return self._last_launched

    @last_launched.setter
    def last_launched(self, new_value: str):
        if self._last_launched != new_value:
            self._last_launched = new_value
            self.last_launched_changed.emit()

    # endregion

    # region Last launched

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

    # region Installation path

    @Property(bool, notify=is_running_changed)
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, new_value: bool):
        if self._is_running == new_value:
            return
        self._is_running = new_value
        self.is_running_changed.emit()

    # endregion

    def _check_game_installed(self, game_id: int) -> bool:
        with open("../app_config.json", "r") as app_config_file:
            config = json.load(app_config_file)
            for app in config["apps"]:
                if game_id == app['game_id']:
                    return True
            return False

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

            self.is_game_installed = self._check_game_installed(data["game"]["id"])

            game_play_time = data["game_time"]
            if game_play_time / 3600 < 1:
                self.play_time = '{00:.0f}'.format(game_play_time // 60)
            else:
                self.play_time = '{0:.1f}'.format(game_play_time / 3600)

            possible_last_launch_stamp: int | None = data["last_run"]
            if possible_last_launch_stamp:
                launch_date = datetime.fromtimestamp(possible_last_launch_stamp)

                if datetime.today().date() == launch_date.date():
                    self.last_launched = "Today"
                elif datetime.today().date() - timedelta(1) == launch_date.date():
                    self.last_launched = "Yesterday"
                else:
                    self.last_launched = launch_date.strftime('%d %b %y')
            else:
                self.last_launched = "Never"

    @Slot()
    def download(self):
        get_builds_url = ''.join(BUILDS_URL + f"?game_id={self._game_id}")
        builds = requests.get(get_builds_url).json()

        platforms = self._auth_service.authorized_session.get(PLATFORMS_URL).json()

        for build in builds:
            platform_id = build['platform_id']
            platform = next((platform for platform in platforms if platform['id'] == platform_id), None)
            if platform:
                if platform['title'] == sys.platform:
                    get_build_filenames = get_builds_url + str(build["id"])
                    filenames = requests.get(get_build_filenames).json()

                    library_path = QUrl(self.installation_path).toLocalFile()
                    game_installation_path = Path(library_path).joinpath(self.game_title)

                    Path.mkdir(game_installation_path, parents=True)

                    for filename in filenames:
                        file_url = get_build_filenames + f'/?filename={filename}'
                        response = requests.get(file_url, stream=True)
                        file_name = response.headers.get("Content-Disposition").split('=')[1]
                        with open(game_installation_path.joinpath(file_name), "wb") as f:
                            with gzip.GzipFile(fileobj=response.raw, mode="rb") as gz:
                                while True:
                                    chunk = gz.read(8192)
                                    if not chunk:
                                        break
                                    f.write(chunk)

                    app_config_file = open("../app_config.json", "r")
                    config = json.load(app_config_file)
                    app_config_file.close()

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

                    self.is_game_installed = True
                break

    @Slot()
    def stop(self):
        self.app.kill()
        self.app.wait()
        self.is_running=False
        self.timer.stop()


    @Slot()
    def run(self):
        with open("../app_config.json", "r") as app_config_file:
            config = json.load(app_config_file)
            apps = config["apps"]

            for app in apps:
                if self._game_id == app['game_id']:
                    process = Path(config["default_games_installation_path"][sys.platform]).joinpath(config["default_library_path_name"], app['path'], app['call'])
                    self.app = subprocess.Popen(process, stdout=subprocess.PIPE)
                    self.is_running = True
                    self.timer.start()
                    self._auth_service.authorized_session.put(LIBRARY_URL + f'{self._id}/', json={
                        "game_time": 1,
                        "last_run": datetime.today().timestamp()
                    })
                    break
