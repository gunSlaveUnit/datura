from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class TagCreateSchema(BaseModel):
    title: str


class TagDBSchema(TagCreateSchema, EntityDBSchema):
    class Config:
        orm_mode = True
