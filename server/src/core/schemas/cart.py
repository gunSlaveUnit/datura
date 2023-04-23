from pydantic import BaseModel

from server.src.core.schemas.entity import EntityDBSchema
from server.src.core.schemas.game import GameDBSchema


class CartCreateSchema(BaseModel):
    game_id: int


class CartDBSchema(EntityDBSchema):
    buyer_id: int
    game_id: int

    class Config:
        orm_mode = True


class CartJoinedSchema(CartDBSchema):
    game: GameDBSchema
