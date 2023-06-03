import os

from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import USERS_URL


class CurrentUserLogic(QObject):
    id_changed = Signal()
    displayed_name_changed = Signal()

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._displayed_name = ''
        self._avatar = ''

    @Property(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value: int):
        if self._id != new_value:
            self._id = new_value
            self.id_changed.emit()

    @Property(str, notify=displayed_name_changed)
    def displayed_name(self):
        return self._displayed_name

    @displayed_name.setter
    def displayed_name(self, new_value: str):
        if self._displayed_name != new_value:
            self._displayed_name = new_value
            self.displayed_name_changed.emit()

    avatar_changed = Signal()

    @Property(str, notify=avatar_changed)
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, new_value: str):
        if self._avatar != new_value:
            self._avatar = new_value
            self.avatar_changed.emit()

    @Slot()
    def map(self):
        self._auth_service.load_current_user()

        self.id = self._auth_service.current_user.id
        self.displayed_name = self._auth_service.current_user.displayed_name

    @Slot()
    def update(self):
        data = {"displayed_name": self._displayed_name}

        url = USERS_URL + f"{self.id}/"
        self._auth_service.authorized_session.put(url, json=data)

        if self._avatar != '':
            filename = QUrl(self._avatar).toLocalFile()
            with open(filename, 'rb') as avatar_file:
                files = [('file', (os.path.basename(filename), avatar_file))]
                url = USERS_URL + f"{self.id}" + '/avatar/'
                self._auth_service.authorized_session.put(url, files=files)
            self._avatar = ''

        self.map()
