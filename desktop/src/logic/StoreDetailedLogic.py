from enum import Enum

from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.models.game import Game
from desktop.src.services.CartService import CartService
from desktop.src.services.GameService import GameService
from desktop.src.services.LibraryService import LibraryService


class GameLocation(int, Enum):
    IN_STORE = 0
    IN_LIBRARY = 1
    IN_CART = 2


class StoreDetailedLogic(QObject):
    id_changed = Signal()
    title_changed = Signal()
    short_description_changed = Signal()
    long_description_changed = Signal()
    price_changed = Signal()

    screenshots_changed = Signal()
    trailers_changed = Signal()

    location_changed = Signal()

    loaded = Signal()

    def __init__(self,
                 game_service: GameService,
                 library_service: LibraryService,
                 cart_service: CartService):
        super().__init__()

        self._game_service: GameService = game_service
        self._library_service: LibraryService = library_service
        self._cart_service: CartService = cart_service

        self._id = -1
        self._title = ''
        self._short_description = ''
        self._long_description = ''
        self._release_date = 0.0
        self._price = 0.0

        self._screenshots = []
        self._trailers = []

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

    # region Short description

    @Property(str, notify=short_description_changed)
    def short_description(self):
        return self._short_description

    @short_description.setter
    def short_description(self, new_value: str):
        if self._short_description != new_value:
            self._short_description = new_value
            self.short_description_changed.emit()

    # endregion

    # region Short description

    @Property(str, notify=long_description_changed)
    def long_description(self):
        return self._long_description

    @long_description.setter
    def long_description(self, new_value: str):
        if self._long_description != new_value:
            self._long_description = new_value
            self.long_description_changed.emit()

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

    release_date_changed = Signal()

    @Property(int, notify=release_date_changed)
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, new_value: int):
        if self._release_date != new_value:
            self._release_date = new_value
            self.release_date_changed.emit()

    # region Screenshots

    @Property(list, notify=screenshots_changed)
    def screenshots(self):
        return self._screenshots

    @screenshots.setter
    def screenshots(self, new_value: list):
        if self._screenshots != new_value:
            self._screenshots = new_value
            self.screenshots_changed.emit()

    # endregion

    # region Trailers

    @Property(list, notify=trailers_changed)
    def trailers(self):
        return self._trailers

    @trailers.setter
    def trailers(self, new_value: list):
        if self._trailers != new_value:
            self._trailers = new_value
            self.trailers_changed.emit()

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

            self.id = game.id
            self.title = game.title
            self.short_description = game.short_description
            self.long_description = game.long_description
            self.price = game.price
            self.release_date = game.release_date

            self._set_game_location_status()

        response = self._game_service.screenshots(game_id)
        if response.ok:
            self.screenshots = response.json()["filenames"]

        response = self._game_service.trailers(game_id)
        if response.ok:
            self.trailers = response.json()["filenames"]

        self.loaded.emit()

    def _set_game_location_status(self):
        if self._library_service.check(item_id=self.id):
            self.location = GameLocation.IN_LIBRARY
        elif self._cart_service.check(item_id=self.id):
            self.location = GameLocation.IN_CART
        else:
            self.location = GameLocation.IN_STORE
