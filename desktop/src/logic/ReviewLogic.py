import requests
from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import GAMES_URL


class ReviewLogic(QObject):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._content = ''
        self._is_recommended = False

    content_changed = Signal()

    @Property(str, notify=content_changed)
    def content(self):
        return self._content

    @content.setter
    def content(self, new_value: str):
        if self._content != new_value:
            self._content = new_value
            self.content_changed.emit()

    is_recommended_changed = Signal()

    @Property(bool, notify=is_recommended_changed)
    def is_recommended(self):
        return self._is_recommended

    @is_recommended.setter
    def is_recommended(self, new_value: bool):
        if self._is_recommended != new_value:
            self._is_recommended = new_value
            self.is_recommended_changed.emit()

    @Slot(int)
    def new(self, game_id: int):
        # TODO: we need to map languages

        review = {
            "content": self._content,
            "is_game_recommended": self._is_recommended,
            "language_id": 1
        }

        params = {"game_id": game_id}
        reply = self._auth_service.authorized_session.post(f'{GAMES_URL}{game_id}/reviews/', params=params, json=review)

        if reply.status_code == requests.codes.ok:
            self.is_recommended = False
            self.content = ''
