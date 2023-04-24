from fastapi import Depends

from server.src.core.logic.game import GameLogic
from server.src.core.models.game import Game
from server.src.core.models.user import User
from server.src.core.utils.db import get_db
from server.src.schemas.game import GameCreateSchema


class GameController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.game_logic = GameLogic(db)

    async def items(self):
        items = await self.game_logic.items()
        return items.all()

    async def create(self, game_data: GameCreateSchema, current_user: User):
        game = Game(**vars(game_data))
        game.owner_id = current_user.id

        return await self.game_logic.create(game)
