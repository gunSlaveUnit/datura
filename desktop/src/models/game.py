from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import LIBRARY_URL, GAMES_URL


@dataclass(slots=True)
class Game(Entity):
    title: str
    release_date: int | None
    developer: str
    publisher: str
    short_description: str
    long_description: str
    price: float
    status_id: int
    age_category_id: int
    directory: str
    company_id: int


class GameList(QAbstractListModel):
    def __init__(self, auth_service: AuthService,
                 company_service: CompanyService):
        super().__init__()

        self._auth_service = auth_service
        self._company_service = company_service

        self._games = []

    @Slot()
    def load_library(self):
        current_user_id = self._auth_service.current_user.id
        headers = {"Authorization": self._auth_service.session_id}

        library_records = requests.get(LIBRARY_URL + f"?user_id={current_user_id}&include_games=true",
                                       headers=headers).json()
        self.beginResetModel()
        self._games = []
        for record in library_records:
            game_data = record["game"]
            self._games.append(Game(**game_data))
        self.endResetModel()

    @Slot()
    def load_store(self):
        headers = {"Authorization": self._auth_service.session_id}

        games = requests.get(GAMES_URL, headers=headers).json()
        self.beginResetModel()
        self._games = []
        for game in games:
            self._games.append(Game(**game))
        self.endResetModel()

    @Slot()
    def load_personal(self):
        self._company_service.load_personal()
        if self._company_service.company is not None:
            url = GAMES_URL + f'?company_id={self._company_service.company["id"]}'
            data = requests.get(url, headers={"Authorization": self._auth_service.session_id}).json()
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
