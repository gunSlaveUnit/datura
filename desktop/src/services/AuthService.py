import requests

from desktop.src.settings import REGISTER_URL, LOGIN_URL, ME_URL, LOGOUT_URL
from desktop.src.utils.singleton import Singleton


class AuthService(metaclass=Singleton):
    def __init__(self):
        super().__init__()

        self.session_id = None
        self.current_user = None

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

    def load_personal_user_data(self):
        headers = {"Authorization": self.session_id}

        reply = requests.get(ME_URL, headers=headers)

        if reply.status_code == requests.codes.ok:
            self.current_user = reply.json()
