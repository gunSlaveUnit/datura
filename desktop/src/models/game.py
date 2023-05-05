from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot, Property, Signal

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import GAMES_URL, CART_URL


@dataclass()
class Game(Entity):
    title: str
    release_date: int | None
    short_description: str
    long_description: str
    price: float
    owner_id: int
    is_approved: bool
    is_send_for_verification: bool
    is_published: bool
    age_category_id: int
    directory: str
    is_checked: bool | None = None


class GameList(QAbstractListModel):
    def __init__(self,
                 auth_service: AuthService,
                 company_service: CompanyService):
        super().__init__()

        self._auth_service = auth_service
        self._company_service = company_service

        self._games = []
        self._total_cost = 0.0

    total_cost_changed = Signal()

    @Property(float, notify=total_cost_changed)
    def total_cost(self):
        return self._total_cost

    @total_cost.setter
    def total_cost(self, new_value: float):
        if self._total_cost != new_value:
            self._total_cost = new_value
            self.total_cost_changed.emit()

    @Slot()
    def load_store(self):
        reply = self._auth_service.authorized_session.get(GAMES_URL)

        if reply.status_code == requests.codes.ok:
            games = reply.json()

            self.beginResetModel()
            self._games = []
            for game in games:
                self._games.append(Game(**game, is_checked=False))
            self.endResetModel()

    @Slot()
    def load_personal(self):
        self._company_service.load_personal()
        if self._company_service.company is not None:
            params = {"company_id": self._company_service.company.id}
            data = self._auth_service.authorized_session.get(GAMES_URL, params = params).json()
            self.beginResetModel()
            self._games = [Game(**detailed_game_data, is_checked=False) for detailed_game_data in data]
            self.endResetModel()

    @Slot()
    def load_cart(self):
        cart_records = self._auth_service.authorized_session.get(CART_URL + "?include_games=true").json()
        self.beginResetModel()
        self._games = []
        for record in cart_records:
            game_data = record["game"]
            self._games.append(Game(**game_data, is_checked=False))
        self.endResetModel()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if 0 <= index.row() < self.rowCount():
            game = self._games[index.row()]
            name = self.roleNames().get(role)
            if name:
                return getattr(game, name.decode())

    def roleNames(self) -> dict[int, QByteArray]:
        d = {}
        for i, field in enumerate(fields(Game)):
            d[Qt.DisplayRole + i] = field.name.encode()
        return d

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._games)

    @Slot(int)
    def change_checked_state(self, index: int):
        self._games[index].is_checked = not self._games[index].is_checked

    @Slot()
    def recount_total_cost(self):
        self.total_cost = 0
        for game in self._games:
            if game.is_checked:
                self.total_cost += game.price
