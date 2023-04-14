from pydantic import BaseModel

from server.src.schemas.entity import EntityDBSchema


class BuildCreateSchema(BaseModel):
    platform_id: int
    call: str
    params: str | None


class BuildDBSchema(BuildCreateSchema, EntityDBSchema):
    game_id: int
    directory: str

    class Config:
        orm_mode = True
