from pydantic import BaseModel

from server.src.schemes.entity import EntityDBScheme


class GameApprovingScheme(BaseModel):
    is_approved: bool


class GameCreateScheme(BaseModel):
    title: str


class GameDBScheme(GameCreateScheme, EntityDBScheme):
    class Config:
        orm_mode = True
