from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema


class BuildCreateSchema(BaseModel):
    game_id: int
    platform_id: int
    version: str
    call: str
    params: str | None


class BuildDBSchema(BuildCreateSchema, EntityDBSchema):
    directory: str

    class Config:
        from_attributes = True
