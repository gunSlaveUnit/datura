from dataclasses import dataclass

from PySide6.QtCore import Property, Signal, QObject

from desktop.src.models.entity import Entity


@dataclass
class User(Entity):
    name_changed = Signal()

    email: str
    account_name: str
    displayed_name: str
    password: str
    is_active: bool
    login_at: int | None
    is_staff: bool
    is_superuser: bool
    avatar: str
    role_id: int
