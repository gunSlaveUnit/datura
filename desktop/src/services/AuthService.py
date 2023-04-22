import requests
from PySide6.QtCore import QObject, Signal, Property

from desktop.src.models.user import User
from desktop.src.settings import REGISTER_URL, LOGIN_URL, ME_URL, LOGOUT_URL


class AuthService(QObject):
    def __init__(self):
        super().__init__()

        self.session_id = None
        self._current_user = None

    @Signal
    def current_user_changed(self):
        pass

    @Property(QObject, notify=current_user_changed)
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, new_value: QObject):
        if self._current_user == new_value:
            return
        self._current_user = new_value
        self.current_user_changed.emit()

    def sign_up(self, data):
        reply = requests.post(REGISTER_URL, json=data)
        if reply.status_code == requests.codes.ok:
            self.session_id = reply.cookies['session_id']
            self.load_personal_user_data()
        return reply

    def sign_in(self, data):
        reply = requests.post(LOGIN_URL, json=data)
        if reply.status_code == requests.codes.ok:
            self.session_id = reply.cookies['session_id']
            self.load_personal_user_data()
        return reply

    def sign_out(self):
        headers = {"Authorization": self.session_id}

        reply = requests.post(LOGOUT_URL, headers=headers)
        if reply.status_code == requests.codes.ok:
            self.session_id = None
            self.current_user = None
        return reply

    def load_personal_user_data(self):
        headers = {"Authorization": self.session_id}

        reply = requests.get(ME_URL, headers=headers)

        if reply.status_code == requests.codes.ok:
            self.current_user = User(**reply.json())
