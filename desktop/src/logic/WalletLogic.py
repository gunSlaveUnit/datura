from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import ME_URL, USERS_URL


class WalletLogic(QObject):
    # region Signals

    balance_changed = Signal()

    # endregion

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._balance = 0.00

    # region Properties

    @Property(float, notify=balance_changed)
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_value: float):
        if self._balance != new_value:
            self._balance = new_value
            self.balance_changed.emit()

    # region Slots

    @Slot(int)
    def load(self, current_user_id: int):
        response = self._auth_service.authorized_session.get(USERS_URL + f'{current_user_id}/balance/')

        if response.ok:
            data = response.json()
            self.balance = data["balance"]

    # endregion
