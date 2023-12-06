from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema


class RequirementsCreateSchema(BaseModel):
    os: str
    processor: str
    memory: str
    storage: str
    graphics: str
    network: str
    extra: str


class RequirementsDBSchema(RequirementsCreateSchema, EntityDBSchema):
    build_id: int

    class Config:
        from_attributes = True
