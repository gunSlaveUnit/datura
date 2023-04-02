from pydantic import BaseModel

from server.src.schemes.entity import EntityDBSchema


class GameApprovingSchema(BaseModel):
    is_approved: bool


class GameCreateSchema(BaseModel):
    title: str


class GameDBSchema(GameCreateSchema, EntityDBSchema):
    class Config:
        orm_mode = True
