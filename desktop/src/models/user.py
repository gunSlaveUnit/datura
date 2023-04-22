import datetime

from PySide6.QtCore import Signal, Property

from desktop.src.models.entity import Entity


class User(Entity):
    loaded = Signal()

    def __init__(self,
                 id: int = -1,
                 created_at: datetime.datetime = -1,
                 last_updated_at: datetime.datetime | None = None,
                 email: str = '',
                 account_name: str = '',
                 displayed_name: str = '',
                 password: str = '',
                 is_active: bool = False,
                 last_login_at: int | None = None,
                 is_staff: bool = False,
                 is_superuser: bool = False,
                 avatar: str = '',
                 role_id: int = -1
                 ):
        super().__init__(id, created_at, last_updated_at)

        self._email = email
        self._account_name = account_name
        self._displayed_name = displayed_name
        self._password = password
        self._is_active = is_active
        self._last_login_at = last_login_at
        self._is_staff = is_staff
        self._is_superuser = is_superuser
        self._avatar = avatar
        self._role_id = role_id

    @Signal
    def displayed_name_changed(self):
        pass

    @Property(str, notify=displayed_name_changed)
    def displayed_name(self):
        return self._displayed_name

    @displayed_name.setter
    def displayed_name(self, new_value: str):
        if self._displayed_name == new_value:
            return
        self._displayed_name = new_value
        self.displayed_name_changed.emit()
