from pydantic import BaseModel

from server.src.schemas.entity import EntityDBSchema


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
    status_id: int
    age_category_id: int


class GameDBSchema(GameCreateSchema, EntityDBSchema):
    directory: str
    company_id: int

    class Config:
        orm_mode = True
