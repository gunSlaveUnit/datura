from PySide6.QtCore import QObject, Slot, Signal, Property

from desktop.src.settings import GAMES_URL, BUILDS_URL, PLATFORMS_URL
from server.src.core.models.platform import Platform


class BuildLogic(QObject):
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._call = ''
        self._params = ''
        self._platform_id = -1

        self._platforms = []

    id_changed = Signal()
    call_changed = Signal()
    params_changed = Signal()
    platform_id_changed = Signal()

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

    @Property(str, notify=params_changed)
    def params(self):
        return self._params

    @params.setter
    def params(self, new_value: str):
        if self._params != new_value:
            self._params = new_value
            self.params_changed.emit()

    @Property(int, notify=platform_id_changed)
    def platform_id(self):
        return self._platform_id

    @platform_id.setter
    def platform_id(self, new_value: int):
        if self._platform_id != new_value:
            self._platform_id = new_value
            self.platform_id_changed.emit()

    def reset_form(self):
        self.id = -1
        self.call = ''
        self.params = ''
        self.platform_id = 1

    drafted = Signal()

    @Slot()
    def load_platforms(self):
        response = self._auth_service.authorized_session.get(PLATFORMS_URL)
        if response.ok:
            platforms = response.json()
            self._platforms = [Platform(**platform) for platform in platforms]
            self.platforms_changed.emit()

    platforms_changed = Signal()

    @Property(list, notify=platforms_changed)
    def displayed_platforms(self):
        return [platform.title for platform in self._platforms]

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
    def map(self, build_id: int):
        response = self._auth_service.authorized_session.get(BUILDS_URL + f'{build_id}/')

        if response.ok:
            data = response.json()

            self.id = data['id']
            self.call = data['call']
            self.params = data['params']
            self.platform_id = data['platform_id']
