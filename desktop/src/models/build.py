from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import GAMES_URL, BUILDS_URL


@dataclass()
class Build(Entity):
    directory: str
    call: str
    params: str | None
    game_id: int
    platform_id: int
    platform_title: str


class BuildList(QAbstractListModel):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._builds = []

    @Slot(int)
    def load_for_game(self, game_id: int):
        response = self._auth_service.authorized_session.get(
            BUILDS_URL + f'?game_id={game_id}&include_platform=true'
        )

        if response.ok:
            builds = response.json()

            self.beginResetModel()
            self._builds = []
            for build_data in builds:
                build = Build(
                    id=build_data['id'],
                    created_at=build_data['created_at'],
                    updated_at=build_data['updated_at'],
                    directory=build_data['directory'],
                    call=build_data['call'],
                    params=build_data['params'],
                    game_id=build_data['game_id'],
                    platform_id=build_data['platform_id'],
                    platform_title=build_data['platform']['title']
                )
                self._builds.append(build)
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
