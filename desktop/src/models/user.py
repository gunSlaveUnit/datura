from dataclasses import dataclass

from desktop.src.models.entity import Entity


@dataclass(slots=True)
class User(Entity):
    id: int
    email: str
    account_name: str
    displayed_name: str
    password: str
    is_active: bool
    last_login_at: int | None
    is_staff: bool
    is_superuser: bool
    avatar: str
    role_id: int
