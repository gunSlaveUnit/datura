from PySide6.QtCore import QObject, Signal, Slot, Property


class AuthLogic(QObject):
    """
    Class containing properties for registration, login screens
    """

    # region Signals

    email_changed = Signal()
    account_name_changed = Signal()
    password_changed = Signal()

    # endregion

    def __init__(self):
        super().__init__()

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
        self.reset()

    @Slot()
    def sign_in(self):
        self.reset()

    @Slot()
    def sign_out(self):
        pass

    @Slot()
    def reset(self):
        self.email = ''
        self.account_name = ''
        self.password = ''

    # endregion
