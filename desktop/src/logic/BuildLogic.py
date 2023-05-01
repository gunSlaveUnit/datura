from PySide6.QtCore import QObject, Slot


class BuildLogic(QObject):
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

    @Slot(int)
    def map(self, game_id: int):
        print(game_id)
