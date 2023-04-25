from server.src.api.v1.schemas.entity import EntityDBSchema


class PlatformDBSchema(EntityDBSchema):
    title: str

    class Config:
        orm_mode = True
