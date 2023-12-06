from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema
from common.api.v1.schemas.game import GameDBSchema


class CartCreateSchema(BaseModel):
    game_id: int


class CartDBSchema(EntityDBSchema):
    buyer_id: int
    game_id: int

    class Config:
        from_attributes = True


class CartJoinedSchema(CartDBSchema):
    game: GameDBSchema
