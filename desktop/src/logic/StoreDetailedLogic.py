from enum import Enum

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import GAMES_URL, LIBRARY_URL, CART_URL


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
        response = self._auth_service.authorized_session.get(GAMES_URL + f'{game_id}/')
        if response.ok:
            data = response.json()

            self._game_id = data["id"]
            self.game_title = data["title"]

            self._set_game_location_status()

    def _set_game_location_status(self):
        if self._check_game_in_library():
            self.game_location = GameLocation.IN_LIBRARY
        elif self._check_game_in_cart():
            self.game_location = GameLocation.IN_CART
        else:
            self.game_location = GameLocation.IN_STORE

    def _check_game_in_library(self):
        user_id = self._auth_service.current_user.id
        response = self._auth_service.authorized_session.get(
            LIBRARY_URL + f"?user_id={user_id}&game_id={self._game_id}"
        )
        return response.ok and response.json()

    def _check_game_in_cart(self):
        response = self._auth_service.authorized_session.get(CART_URL + f'?game_id={self._game_id}')
        return response.ok and response.json()
