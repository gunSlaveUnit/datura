from typing import Union

import requests
from PySide6.QtCore import QObject, Signal, Property

from desktop.src.schemas.auth import SignInSchema, SignUpSchema
from desktop.src.settings import REGISTER_URL, LOGIN_URL, LOGOUT_URL


class AuthService(QObject):
    current_user_changed = Signal()

    def __init__(self):
        super().__init__()

        self.authorized_session = None
        self._current_user = None

    @Property(QObject, notify=current_user_changed)
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, new_value: QObject):
        if self._current_user != new_value:
            self._current_user = new_value
            self.current_user_changed.emit()

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
