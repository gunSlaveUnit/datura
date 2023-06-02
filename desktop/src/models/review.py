from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.settings import REVIEWS_URL


@dataclass()
class Review(Entity):
    is_game_recommended: bool
    language_id: int
    game_id: int
    content: str
    user_id: int


class ReviewList(QAbstractListModel):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._reviews = []

    @Slot(int)
    def load(self, game_id: int):
        params = {"game_id": game_id}
        reply = self._auth_service.authorized_session.get(REVIEWS_URL, params=params)

        if reply.status_code == requests.codes.ok:
            reviews = reply.json()

            self.beginResetModel()
            self._reviews = []
            for review in reviews:
                self._reviews.append(Review(**review))
            self.endResetModel()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if 0 <= index.row() < self.rowCount():
            review = self._reviews[index.row()]
            name = self.roleNames().get(role)
            if name:
                return getattr(review, name.decode())

    def roleNames(self) -> dict[int, QByteArray]:
        d = {}
        for i, field in enumerate(fields(Review)):
            d[Qt.DisplayRole + i] = field.name.encode()
        return d

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._reviews)
