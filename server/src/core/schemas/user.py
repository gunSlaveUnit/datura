import datetime

from server.src.core.schemas.entity import EntityDBSchema


class UserDBSchema(EntityDBSchema):
    email: str
    account_name: str
    displayed_name: str
    password: str
    is_active: bool = True
    last_login_at: datetime.datetime | None
    is_staff: bool = False
    is_superuser: bool = False
    role_id: int
    avatar: str

    class Config:
        orm_mode = True
