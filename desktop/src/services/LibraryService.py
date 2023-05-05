from typing import Optional

from PySide6.QtCore import QObject

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL


class LibraryService(QObject):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service: AuthService = auth_service

    def check(self, item_id: int, user_id: Optional[int] = None):
        params = {
            "user_id": user_id if user_id is not None else self._auth_service.current_user.id,
            "game_id": item_id
        }
        response = self._auth_service.authorized_session.get(LIBRARY_URL, params=params)
        return response.ok and response.json()
