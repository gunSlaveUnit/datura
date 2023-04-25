from fastapi import APIRouter, Body, Depends
from starlette import status
from starlette.responses import Response

from server.src.core.controllers.game import GameController
from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.models.user import User
from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GameStatusType
from server.src.core.utils.auth import get_current_user
from server.src.core.utils.db import get_db
from server.src.schemas.game import GameFilterSchema, GameCreateSchema, GameApprovingSchema, GameSendingSchema, \
    GamePublishingSchema
from server.src.api.v1.endpoints.assets import router as assets_router

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])
router.include_router(assets_router)


@router.get('/')
async def items(game_filter: GameFilterSchema = Body(None),
                db=Depends(get_db)):
    published_status = await GameStatus.by_title(db, GameStatusType.PUBLISHED)

    if game_filter is None:
        game_filter = GameFilterSchema(status_id=[published_status.id])

    if game_filter.status_id is None:
        game_filter.status_id = [published_status.id]

    games = db.query(Game).filter(Game.status_id.in_(game_filter.status_id))

    return games.all()


@router.post('/')
async def create(new_game_data: GameCreateSchema,
                 current_user: User = Depends(get_current_user),
                 game_controller: GameController = Depends(GameController)):
    return await game_controller.create(new_game_data, current_user)


@router.patch('/{game_id}/verify/')
async def verify(game_id: int,
                 sending: GameSendingSchema,
                 game_controller: GameController = Depends(GameController)) -> Response:
    """Sends a game for verification."""

    await game_controller.manage_verification(game_id, sending)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/approve/')
async def approve(game_id: int,
                  approving: GameApprovingSchema,
                  game_controller: GameController = Depends(GameController)) -> Response:
    """If it denies, the game becomes not sent for verification."""

    await game_controller.manage_approving(game_id, approving)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/publish/')
async def publish(game_id: int,
                  publishing: GamePublishingSchema,
                  game_controller: GameController = Depends(GameController)) -> Response:
    """
    Publishes the game.
    After that, it is available for downloading.
    """

    await game_controller.manage_publishing(game_id, publishing)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
