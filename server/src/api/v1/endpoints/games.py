from fastapi import APIRouter, Body, Depends
from starlette import status
from starlette.responses import Response

from server.src.core.controllers.game import GameController
from server.src.core.models.user import User
from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GameStatusType
from server.src.core.utils.auth import get_current_user
from server.src.schemas.game import GameFilterSchema, GameCreateSchema, GameApprovingSchema, GameSendingSchema, \
    GamePublishingSchema

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])


# TODO: permissions
@router.get('/')
async def items(game_filter: GameFilterSchema = Body(None),
                game_controller: GameController = Depends(GameController)):
    return await game_controller.items(game_filter)


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
