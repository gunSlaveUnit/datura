from typing import List

from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class GameApprovingSchema(BaseModel):
    is_approved: bool


class GameSendingSchema(BaseModel):
    is_send: bool


class GamePublishingSchema(BaseModel):
    is_published: bool


class GameFilterSchema(BaseModel):
    title: str = None
    start_date: int = None
    end_date: int = None
    start_price: float = None
    end_price: float = None
    tag_id: List[int] = None
    status_id: List[int] = None
    age_category_id: List[int] = None


class GameCreateSchema(BaseModel):
    title: str
    release_date: int | None
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
