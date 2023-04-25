import uuid

from fastapi import Depends, HTTPException
from starlette import status

from server.src.core.logic.company import CompanyLogic
from server.src.core.logic.game import GameLogic
from server.src.core.logic.game_status import GameStatusLogic
from server.src.core.models.game import Game
from server.src.core.models.user import User
from server.src.core.settings import GAMES_ASSETS_PATH, GameStatusType, GAMES_ASSETS_CAPSULE_DIR, \
    GAMES_ASSETS_SCREENSHOTS_DIR, GAMES_ASSETS_BUILDS_DIR, GAMES_ASSETS_HEADER_DIR, GAMES_ASSETS_TRAILERS_DIR
from server.src.core.utils.db import get_db
from server.src.schemas.game import GameCreateSchema, GameFilterSchema, GameApprovingSchema, GamePublishingSchema


class GameController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.game_logic = GameLogic(db)
        self.company_logic = CompanyLogic(db)
        self.game_status_logic = GameStatusLogic(db)

    async def manage_publishing(self, game_id: int, publishing: GamePublishingSchema):
        try:
            game = await self.game_logic.item_by_id(game_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game with this id not found"
            )

        not_published_status = await self.game_status_logic.item_by_title(GameStatusType.NOT_PUBLISHED)
        if game.status_id != not_published_status.id and publishing.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The game cannot be published because it was not previously published or was not previously "
                       "submitted for review"
            )

        new_game_status = await self.game_status_logic.item_by_title(
            GameStatusType.PUBLISHED if publishing.is_published else GameStatusType.NOT_PUBLISHED
        )

        await self.game_logic.update(game_id, {"status_id": new_game_status.id})
