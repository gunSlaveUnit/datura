from enum import Enum

from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.models.game import Game
from desktop.src.services.GameService import GameService
from desktop.src.settings import LIBRARY_URL, CART_URL


class GameLocation(int, Enum):
    IN_STORE = 0
    IN_LIBRARY = 1
    IN_CART = 2


class StoreDetailedLogic(QObject):
    id_changed = Signal()
    title_changed = Signal()
    price_changed = Signal()
    location_changed = Signal()

    def __init__(self, game_service: GameService):
        super().__init__()

        self._game_service = game_service

        self._id = -1
        self._title = ''
        self._price = 0.0
        self._location: int = GameLocation.IN_STORE

    # region Title

    @Property(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value: int):
        if self._id != new_value:
            self._id = new_value
            self.id_changed.emit()

    # endregion

    # region Title

    @Property(str, notify=title_changed)
    def title(self):
        return self._title

    @title.setter
    def title(self, new_value: str):
        if self._title != new_value:
            self._title = new_value
            self.title_changed.emit()

    # endregion

    # region Price

    @Property(float, notify=price_changed)
    def price(self):
        return self._price

    @price.setter
    def price(self, new_value: float):
        if self._price != new_value:
            self._price = new_value
            self.price_changed.emit()

    # endregion

    # region Location

    @Property(int, notify=location_changed)
    def location(self):
        return self._location

    @location.setter
    def location(self, new_value: int):
        if self._location != new_value:
            self._location = new_value
            self.location_changed.emit()

    # endregion

    @Slot(int)
    def map(self, game_id: int):
        response = self._game_service.item(game_id)

        if response.ok:
            game = Game(**response.json())

            self._id = game.id
            self.title = game.title
            self.price = game.price

            self._set_game_location_status()

    def _set_game_location_status(self):
        if self._check_game_in_library():
            self.location = GameLocation.IN_LIBRARY
        elif self._check_game_in_cart():
            self.location = GameLocation.IN_CART
        else:
            self.location = GameLocation.IN_STORE

    def _check_game_in_library(self):
        user_id = self._auth_service.current_user.id
        response = self._auth_service.authorized_session.get(
            LIBRARY_URL + f"?user_id={user_id}&game_id={self._id}"
        )
        return response.ok and response.json()

    def _check_game_in_cart(self):
        response = self._auth_service.authorized_session.get(CART_URL + f'?game_id={self._id}')
        return response.ok and response.json()
