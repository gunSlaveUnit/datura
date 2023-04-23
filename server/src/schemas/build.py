from pydantic import BaseModel

from server.src.schemas.entity import EntityDBSchema
from server.src.schemas.platform import PlatformDBSchema


class BuildCreateSchema(BaseModel):
    platform_id: int
    call: str
    params: str | None


class BuildDBSchema(BuildCreateSchema, EntityDBSchema):
    game_id: int
    directory: str
    platform: PlatformDBSchema | None

    class Config:
        orm_mode = True
