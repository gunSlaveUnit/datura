import gzip
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL, GAMES_URL, BUILDS_URL_PART, ASSETS_URL_PART


class StoreDetailedLogic(QObject):
    game_title_changed = Signal()

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._game_id = -1
        self._game_title = ''

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

    @Slot(int)
    def load(self, game_id: int):
        headers = {"Authorization": self._auth_service.session_id}

        reply = requests.get(GAMES_URL + f'{game_id}/', headers=headers)
        if reply.status_code == requests.codes.ok:
            data = reply.json()

            self._game_id = data["id"]
            self.game_title = data["title"]
