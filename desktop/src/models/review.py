from dataclasses import fields, dataclass
from typing import Any

import requests
from PySide6.QtCore import QAbstractListModel, QModelIndex, QByteArray, Qt, Slot, Signal, Property

from desktop.src.models.entity import Entity
from desktop.src.services.AuthService import AuthService
from desktop.src.settings import GAMES_URL


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
        self._rating = 0.0

    @Slot(int)
    def load(self, game_id: int):
        params = {"game_id": game_id}
        reply = self._auth_service.authorized_session.get(f'{GAMES_URL}{game_id}/reviews/', params=params)

        if reply.status_code == requests.codes.ok:
            reviews = reply.json()

            self.beginResetModel()
            self._reviews = []
            for review in reviews:
                self._reviews.append(Review(**review))
            self.endResetModel()

            total_reviews = len(self._reviews)
            recommended_reviews = sum(review.is_game_recommended for review in self._reviews)

            self.rating = recommended_reviews / total_reviews

    rating_changed = Signal()

    @Property(float, notify=rating_changed)
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, new_value: float):
        if self._rating != new_value:
            self._rating = new_value
            self.rating_changed.emit()

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
