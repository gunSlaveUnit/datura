from typing import Optional

from PySide6.QtCore import QObject

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import LIBRARY_URL, CART_URL


class CartService(QObject):
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service: AuthService = auth_service

    def check(self, item_id: int):
        params = {"game_id": item_id}
        response = self._auth_service.authorized_session.get(CART_URL, params=params)
        return response.ok and response.json()

    def add(self, item_id):
        json = {"game_id": item_id}
        response = self._auth_service.authorized_session.post(CART_URL, json=json)
        return response
