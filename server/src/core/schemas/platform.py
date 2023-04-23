from server.src.core.schemas.entity import EntityDBSchema


class PlatformDBSchema(EntityDBSchema):
    title: str

    class Config:
        orm_mode = True
