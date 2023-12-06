from common.api.v1.schemas.entity import EntityDBSchema


class PlatformDBSchema(EntityDBSchema):
    title: str

    class Config:
        from_attributes = True
