from typing import Union, Optional

import requests
from PySide6.QtCore import QObject, Slot

from common.api.v1.schemas.auth import SignUpSchema, SignInSchema
from desktop.src.models.user import User
from desktop.src.settings import REGISTER_URL, LOGIN_URL, LOGOUT_URL, ME_URL


class AuthService(QObject):
    def __init__(self):
        super().__init__()

        self.authorized_session = None
        self.current_user: Optional[User] = None

    def _user_access(self, url: str, data: Union[SignUpSchema, SignInSchema]):
        response = requests.post(url, json=data.dict())

        if response.ok:
            self.authorized_session = requests.session()
            self.authorized_session.cookies.set('session', response.cookies['session'])

        return response

    def sign_up(self, data: SignUpSchema):
        return self._user_access(REGISTER_URL, data)

    def sign_in(self, data: SignInSchema):
        return self._user_access(LOGIN_URL, data)

    def sign_out(self):
        response = self.authorized_session.post(LOGOUT_URL)

        if response.ok:
            self.authorized_session = None
            self.current_user = None

        return response

    @Slot()
    def load_current_user(self):
        response = self.authorized_session.get(ME_URL)

        if response.ok:
            self.current_user = User(**response.json())
