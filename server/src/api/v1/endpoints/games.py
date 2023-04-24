from fastapi import APIRouter, Body, Depends

from server.src.core.controllers.game import GameController
from server.src.core.models.user import User
from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GameStatusType
from server.src.core.utils.auth import get_current_user
from server.src.schemas.game import GameFilterSchema, GameCreateSchema

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])


# TODO: permissions
@router.get('/')
async def items(game_filter: GameFilterSchema = Body(None)):
    if game_filter is None:
        game_filter = GameFilterSchema(status_id=[GameStatusType.PUBLISHED])

    return game_filter


@router.post('/')
async def create(new_game_data: GameCreateSchema,
                 current_user: User = Depends(get_current_user),
                 game_controller: GameController = Depends(GameController)):
    return await game_controller.create(new_game_data, current_user)
