from fastapi import APIRouter, Body

from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GameStatusType
from server.src.schemas.game import GameFilterSchema

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])


# TODO: permissions
@router.get('/')
async def items(game_filter: GameFilterSchema = Body(None)):
    if game_filter is None:
        game_filter = GameFilterSchema(status_id=[GameStatusType.PUBLISHED])

    return game_filter
