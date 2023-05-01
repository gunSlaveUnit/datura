from PySide6.QtCore import QObject, Slot, Signal, Property

from desktop.src.settings import GAMES_URL


class BuildLogic(QObject):
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._call = ''

    call_changed = Signal()

    @Property(str, notify=call_changed)
    def call(self):
        return self._call

    @call.setter
    def call(self, new_value: str):
        if self._call != new_value:
            self._call = new_value
            self.call_changed.emit()

    @Slot(int)
    def map(self, game_id, build_id: int):
        response = self._auth_service.authorized_session.get(GAMES_URL + f'{game_id}/builds/{build_id}/')

        if response.ok:
            data = response.json()

            self.call = data['call']
