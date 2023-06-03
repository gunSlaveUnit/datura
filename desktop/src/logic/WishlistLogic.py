from PySide6.QtCore import QObject, Slot

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import WISHLIST_URL


class WishlistLogic(QObject):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

    @Slot(int)
    def new(self, game_id: int):
        record = {
            "user_id": self._auth_service.current_user.id,
            "game_id": game_id
        }

        response = self._auth_service.authorized_session.post(f'{WISHLIST_URL}', json=record)

        if response.ok:
            pass
