from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import GAMES_URL


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


class GameList(QAbstractListModel):
    def __init__(self,
                 auth_service: AuthService,
                 company_service: CompanyService):
        super().__init__()

        self._auth_service = auth_service
        self._company_service = company_service

        self._games = []

    @Slot()
    def load_store(self):
        reply = self._auth_service.authorized_session.get(GAMES_URL)

        if reply.status_code == requests.codes.ok:
            games = reply.json()

            self.beginResetModel()
            self._games = []
            for game in games:
                self._games.append(Game(**game))
            self.endResetModel()

    @Slot(int)
    def load_personal(self, current_user_id):
        self._company_service.load_personal(current_user_id)
        if self._company_service.company is not None:
            url = GAMES_URL + f'?company_id={self._company_service.company["id"]}'
            data = self._auth_service.authorized_session.get(url).json()
            self.beginResetModel()
            self._games = [Game(**detailed_game_data) for detailed_game_data in data]
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
