from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import GAMES_URL


@dataclass()
class Build(Entity):
    directory: str
    call: str
    params: str | None
    game_id: int
    platform_id: int


class BuildList(QAbstractListModel):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._builds = []

    @Slot(int)
    def load_for_game(self, game_id: int):
        response = self._auth_service.authorized_session.get(GAMES_URL + f'{game_id}/builds/')

        if response.ok:
            builds = response.json()

            self.beginResetModel()
            self._builds = []
            for build in builds:
                self._builds.append(Build(**build))
            self.endResetModel()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if 0 <= index.row() < self.rowCount():
            build = self._builds[index.row()]
            name = self.roleNames().get(role)
            if name:
                return getattr(build, name.decode())

    def roleNames(self) -> dict[int, QByteArray]:
        d = {}
        for i, field in enumerate(fields(Build)):
            d[Qt.DisplayRole + i] = field.name.encode()
        return d

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._builds)
