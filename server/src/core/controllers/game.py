import uuid

from fastapi import Depends, HTTPException
from starlette import status

from server.src.core.logic.company import CompanyLogic
from server.src.core.logic.game import GameLogic
from server.src.core.logic.game_status import GameStatusLogic
from server.src.core.models.game import Game
from server.src.core.models.user import User
from server.src.core.settings import GAMES_ASSETS_PATH, GameStatusType
from server.src.core.utils.db import get_db
from server.src.schemas.game import GameCreateSchema, GameFilterSchema, GameApprovingSchema


class GameController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.game_logic = GameLogic(db)
        self.company_logic = CompanyLogic(db)
        self.game_status_logic = GameStatusLogic(db)

    async def items(self, game_filter: GameFilterSchema):
        published_status = await self.game_status_logic.item_by_title(GameStatusType.PUBLISHED)

        if game_filter is None:
            game_filter = GameFilterSchema(status_id=[published_status.id])

        if game_filter.status_id is None:
            game_filter.status_id = [published_status.id]

        items = await self.game_logic.items()

        items = items.filter(Game.status_id.in_(game_filter.status_id))

        return items.all()

    async def create(self, game_data: GameCreateSchema, current_user: User):
        potentially_not_existing_company = await self.company_logic.item_by_owner(current_user.id)

        if potentially_not_existing_company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current user does not have a registered company"
            )

        if not potentially_not_existing_company.is_approved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Information about the user's company may be inaccurate. Creating is temporarily disabled"
            )

        game = Game(**vars(game_data))
        game.owner_id = current_user.id

        not_send_status = await self.game_status_logic.item_by_title(GameStatusType.NOT_SEND)
        game.status_id = not_send_status.id

        new_directory_uuid = str(uuid.uuid4())
        assets_directory = GAMES_ASSETS_PATH.joinpath(new_directory_uuid)
        assets_directory.mkdir(parents=True)
        game.directory = new_directory_uuid

        return await self.game_logic.create(game)

    async def manage_verification(self, game_id, sending):
        new_game_status = await self.game_status_logic.item_by_title(
            GameStatusType.SEND if sending.is_send else GameStatusType.NOT_SEND
        )

        try:
            await self.game_logic.update(game_id, {"status_id": new_game_status.id})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game with this id not found"
            )

    async def manage_approving(self, game_id: int, approving: GameApprovingSchema):
        new_game_status = await self.game_status_logic.item_by_title(
            GameStatusType.NOT_PUBLISHED if approving.is_approved else GameStatusType.NOT_SEND
        )

        try:
            await self.game_logic.update(game_id, {"status_id": new_game_status.id})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game with this id not found"
            )
