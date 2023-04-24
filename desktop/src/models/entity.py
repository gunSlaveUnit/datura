from dataclasses import dataclass

from PySide6.QtCore import QObject


@dataclass()
class Entity(QObject):
    id: int
    created_at: int
    updated_at: int | None
