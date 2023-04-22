import datetime
import inspect
from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import LIBRARY_URL, GAMES_URL


class Game(Entity):
    def __init__(self,
                 id: int = -1,
                 created_at: datetime.datetime = -1,
                 last_updated_at: datetime.datetime | None = None,
                 title: str = '',
                 release_date: int | None = None,
                 developer: str = '',
                 publisher: str = '',
                 short_description: str = '',
                 long_description: str = '',
                 price: float = 0.0,
                 status_id: int = -1,
                 age_category_id: int = -1,
                 directory: str = '',
                 company_id: int = -1
                 ):
        super().__init__(id, created_at, last_updated_at)

        self._title = title
        self._release_date = release_date
        self._developer = developer
        self._publisher = publisher
        self._short_description = short_description
        self._long_description = long_description
        self._price = price
        self._status_id = status_id
        self._age_category_id = age_category_id
        self._directory = directory
        self._company_id = company_id


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

        attributes = inspect.getmembers(Game, lambda a: not (inspect.isroutine(a)))
        attributes = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]

        for i, field in enumerate(attributes):
            d[Qt.DisplayRole + i] = field[0].encode()

        return d

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._games)
