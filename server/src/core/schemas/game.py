from pydantic import BaseModel

from server.src.core.schemas.entity import EntityDBSchema


class GameApprovingSchema(BaseModel):
    is_approved: bool


class GameCreateSchema(BaseModel):
    title: str
    release_date: int | None
    developer: str
    publisher: str
    short_description: str
    long_description: str
    price: float
    age_category_id: int


class GameDBSchema(GameCreateSchema, EntityDBSchema):
    status_id: int
    directory: str
    company_id: int

    class Config:
        orm_mode = True
