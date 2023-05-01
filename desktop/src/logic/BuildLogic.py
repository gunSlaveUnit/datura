from PySide6.QtCore import QObject, Slot, Signal, Property

from desktop.src.settings import GAMES_URL


class BuildLogic(QObject):
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._call = ''

    id_changed = Signal()
    call_changed = Signal()

    @Property(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value: int):
        if self._id != new_value:
            self._id = new_value
            self.id_changed.emit()

    @Property(str, notify=call_changed)
    def call(self):
        return self._call

    @call.setter
    def call(self, new_value: str):
        if self._call != new_value:
            self._call = new_value
            self.call_changed.emit()

    def reset_form(self):
        self.id = -1
        self.call = ''

    drafted = Signal()

    @Slot(int)
    def draft_new(self, game_id: int):
        self.reset_form()

        # TODO: need to get available platforms
        data = {
            "call": self._call,
            "params": None,
            "platform_id": 1
        }

        response = self._auth_service.authorized_session.post(
            GAMES_URL + f'{game_id}/builds/',
            json=data
        )
        if response.ok:
            self.id = response.json()["id"]
            self.drafted.emit()

    @Slot(int)
    def map(self, game_id, build_id: int):
        response = self._auth_service.authorized_session.get(GAMES_URL + f'{game_id}/builds/{build_id}/')

        if response.ok:
            data = response.json()

            self.id = data['id']
            self.call = data['call']
