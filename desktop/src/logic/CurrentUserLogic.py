from PySide6.QtCore import QObject, Signal, Slot, Property

from desktop.src.services.AuthService import AuthService
from desktop.src.settings import ME_URL


class CurrentUserLogic(QObject):
    # region Signals

    id_changed = Signal()
    displayed_name_changed = Signal()

    # endregion

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._displayed_name = ''

    # region Properties

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

    # endregion

    # region Slots

    @Slot()
    def load(self):
        response = self._auth_service.authorized_session.get(ME_URL)

        if response.ok:
            data = response.json()
            self.id = data["id"]
            self.displayed_name = data["displayed_name"]

    # endregion
