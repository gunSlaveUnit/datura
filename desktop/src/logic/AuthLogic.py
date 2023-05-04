from PySide6.QtCore import QObject, Signal, Slot, Property

from common.api.v1.schemas.auth import SignUpSchema, SignInSchema
from desktop.src.services.AuthService import AuthService


class AuthLogic(QObject):
    """
    Class containing properties for registration, login screens
    """

    # region Signals

    email_changed = Signal()
    account_name_changed = Signal()
    password_changed = Signal()

    registered = Signal()
    login = Signal()
    logout = Signal()

    # endregion

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._email = ''
        self._account_name = ''
        self._password = ''

    # region Properties
    @Property(str, notify=email_changed)
    def email(self):
        return self._email

    @email.setter
    def email(self, new_value: str):
        if self._email != new_value:
            self._email = new_value
            self.email_changed.emit()

    @Property(str, notify=account_name_changed)
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, new_value: str):
        if self._account_name != new_value:
            self._account_name = new_value
            self.account_name_changed.emit()

    @Property(str, notify=password_changed)
    def password(self):
        return self._password

    @password.setter
    def password(self, new_value: str):
        if self._password != new_value:
            self._password = new_value
            self.password_changed.emit()

    # endregion

    # region Slots

    @Slot()
    def sign_up(self):
        data = SignUpSchema(
            email=self._email,
            account_name=self._account_name,
            password=self._password
        )

        if self._auth_service.sign_up(data).ok:
            self.registered.emit()
            self.reset()

    @Slot()
    def sign_in(self):
        data = SignInSchema(
            account_name=self._account_name,
            password=self._password
        )

        if self._auth_service.sign_in(data).ok:
            self.login.emit()
            self.reset()

    @Slot()
    def sign_out(self):
        if self._auth_service.sign_out().ok:
            self.logout.emit()

    @Slot()
    def reset(self):
        self.email = ''
        self.account_name = ''
        self.password = ''

    # endregion
