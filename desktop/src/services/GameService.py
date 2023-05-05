from PySide6.QtCore import QObject

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import GAMES_URL


class GameService(QObject):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service: AuthService = auth_service

    def item(self, item_id: int):
        return self._auth_service.authorized_session.get(GAMES_URL + f'{item_id}/')
