from server.src.schemas.entity import EntityDBSchema
from server.src.schemas.game import GameDBSchema


class LibraryDBSchema(EntityDBSchema):
    player_id: int
    game_id: int
    game_time: int
    last_run: int | None

    class Config:
        orm_mode = True


class LibraryJoinedSchema(LibraryDBSchema):
    game: GameDBSchema
