from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
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
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._games = []

    @Slot()
    def load_library(self):
        current_user_id = self._auth_service.current_user["id"]
        headers = {"Authorization": self._auth_service.session_id}

        library_records = requests.get(LIBRARY_URL + f"?user_id={current_user_id}&include_games=true", headers=headers).json()
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
