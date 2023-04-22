import gzip
import json
import subprocess
import sys
from datetime import datetime, timedelta
from enum import auto, Enum
from pathlib import Path

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL, GAMES_URL, BUILDS_URL_PART, ASSETS_URL_PART, CART_URL


class GameLocation(int, Enum):
    IN_STORE = 0
    IN_LIBRARY = 1
    IN_CART = 2


class StoreDetailedLogic(QObject):
    game_title_changed = Signal()
    game_location_changed = Signal()

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._game_id = -1
        self._game_title = ''
        self._game_location: int = GameLocation.IN_STORE

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

    # region Game location

    @Property(int, notify=game_location_changed)
    def game_location(self):
        return self._game_location

    @game_location.setter
    def game_location(self, new_value: int):
        if self._game_location != new_value:
            self._game_location = new_value
            self.game_location_changed.emit()

    # endregion

    @Slot(int)
    def load(self, game_id: int):
        headers = {"Authorization": self._auth_service.session_id}

        reply = requests.get(GAMES_URL + f'{game_id}/', headers=headers)
        if reply.status_code == requests.codes.ok:
            data = reply.json()

            self._game_id = data["id"]
            self.game_title = data["title"]

            reply = requests.get(LIBRARY_URL + f"?user_id={self._auth_service.current_user.id}&game_id={game_id}",
                                 headers=headers)
            if reply.json():
                self.game_location = GameLocation.IN_LIBRARY
            else:
                reply = requests.get(CART_URL + f'?game_id={game_id}', headers=headers)
                if reply.json():
                    self.game_location = GameLocation.IN_CART
