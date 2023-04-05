import datetime

from pydantic import BaseModel

from server.src.schemas.entity import EntityDBSchema


class SignInSchema(BaseModel):
    account_name: str
    password: str


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

    class Config:
        orm_mode = True
