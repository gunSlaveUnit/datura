import datetime

from common.api.v1.schemas.entity import EntityDBSchema


class UserUpdateSchema(EntityDBSchema):
    displayed_name: str


class UserDBSchema(UserUpdateSchema):
    email: str
    account_name: str
    password: str
    is_active: bool = True
    last_login_at: datetime.datetime | None
    is_staff: bool = False
    is_superuser: bool = False
    role_id: int

    class Config:
        orm_mode = True
