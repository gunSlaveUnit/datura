import datetime

from PySide6.QtCore import QObject, Signal, Property


class Entity(QObject):
    def __init__(self,
                 id: int = -1,
                 created_at: datetime.datetime = 0,
                 last_updated_at: datetime.datetime | None = None
                 ):
        super().__init__()

        self._id = id
        self._created_at = created_at
        self._last_updated_at = last_updated_at

    @Signal
    def id_changed(self):
        pass

    @Property(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value: int):
        if self._id == new_value:
            return
        self._id = new_value
        self.id_changed.emit()
