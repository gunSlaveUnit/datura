import json
from enum import Enum, auto
from datetime import datetime, timedelta

from PySide6.QtCore import QObject, Slot, Signal, Property

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL


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

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._id = None
        self._auth_service = auth_service

        self._app_status = self.AppStatus.NOT_INSTALLED
        self._game_id = -1
        self._game_title = ''
        self._last_launched = ''
        self._play_time = ''

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
                self.app_status = self.AppStatus.INSTALLED

            game_play_time = data["game_time"]
            if game_play_time < 3600:
                self.play_time = f"{game_play_time // 60} m"
            else:
                self.play_time = f"{game_play_time / 3600:.1f} h"

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
