from pydantic import BaseModel

from common.api.v1.schemas.entity import EntityDBSchema
from common.api.v1.schemas.game import GameDBSchema


class LibraryUpdateSchema(BaseModel):
    game_time: int
    last_run: int | None

    class Config:
        orm_mode = True


class LibraryDBSchema(EntityDBSchema):
    player_id: int
    game_id: int
    game_time: int
    last_run: int | None

    class Config:
        orm_mode = True


class LibraryJoinedSchema(LibraryDBSchema):
    game: GameDBSchema
