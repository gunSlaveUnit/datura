from typing import List

from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema


class GameApprovingSchema(BaseModel):
    is_approved: bool


class GameSendingSchema(BaseModel):
    is_send_for_verification: bool


class GamePublishingSchema(BaseModel):
    is_published: bool


class GameFilterSchema(BaseModel):
    title: str = None
    start_date: int = None
    end_date: int = None
    start_price: float = None
    end_price: float = None
    tag_id: List[int] = None
    is_approved: bool = None
    is_send_for_verification: bool = None
    is_published: bool = None
    age_category_id: List[int] = None


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
    is_approved: bool
    is_send_for_verification: bool
    is_published: bool
    directory: str
    owner_id: int

    class Config:
        from_attributes = True
