from datetime import datetime

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL


class LibraryDetailedLogic(QObject):
    game_title_changed = Signal()
    is_game_installed_changed = Signal()

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._game_title = ''
        self._is_game_installed = False
        self._last_launched = False

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

    @Property(str, notify=is_game_installed_changed)
    def is_game_installed(self):
        return self._is_game_installed

    @is_game_installed.setter
    def is_game_installed(self, new_value: str):
        if self._is_game_installed != new_value:
            self._is_game_installed = new_value
            self.is_game_installed_changed.emit()

    # endregion

    @Slot(int)
    def load(self, game_id: int):
        headers = {"Authorization": self._auth_service.session_id}
        current_user_id = self._auth_service.current_user["id"]

        reply = requests.get(LIBRARY_URL + f"?user_id={current_user_id}&game_id={game_id}", headers=headers)
        if reply.status_code == requests.codes.ok:
            data = reply.json()[0]

            self.game_title = data["game"]["title"]

    @Slot()
    def download(self):
        pass

    @Slot()
    def run(self):
        pass
