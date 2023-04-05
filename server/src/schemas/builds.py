from pydantic import BaseModel

from server.src.schemes.entity import EntityDBSchema


class BuildCreateSchema(BaseModel):
    platform: int
    call: str
    params: str


class BuildDBSchema(BuildCreateSchema, EntityDBSchema):
    game_id: int
    directory: str

    class Config:
        orm_mode = True
