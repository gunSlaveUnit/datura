from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema


class TagCreateSchema(BaseModel):
    title: str


class GameTagAssociationCreateSchema(BaseModel):
    tag_id: int


class TagDBSchema(TagCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
