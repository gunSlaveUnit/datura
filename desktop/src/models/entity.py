import datetime
from dataclasses import dataclass

from PySide6.QtCore import QObject


@dataclass()
class Entity(QObject):
    id: int
    created_at: int
    last_updated_at: int | None
