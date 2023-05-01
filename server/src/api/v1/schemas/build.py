from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class BuildCreateSchema(BaseModel):
    game_id: int
    platform_id: int
    call: str
    params: str | None


class BuildDBSchema(BuildCreateSchema, EntityDBSchema):
    directory: str

    class Config:
        orm_mode = True
