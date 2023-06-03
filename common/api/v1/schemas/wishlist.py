from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema


class WishlistCreateSchema(BaseModel):
    user_id: int
    game_id: int


class WishlistDBSchema(EntityDBSchema):
    class Config:
        orm_mode = True
