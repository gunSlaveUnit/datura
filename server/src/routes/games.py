from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from server.src.schemes.games import GameCreateSchema, GameDBSchema, GameApprovingSchema
from server.src.settings import GAMES_ROUTER_PREFIX, Tags
from server.src.routes.assets import router as assets_router

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])
router.include_router(assets_router)


@router.get('/', response_model=List[GameDBSchema])
async def every() -> List[GameDBSchema]:
    """
    List of all games according to the given filters.
    Returns a list of GameDBScheme with game data.
    """

    return [
        GameDBSchema(title="Test game title 1"),
        GameDBSchema(title="Test game title 2"),
    ]


@router.post('/', response_model=GameDBSchema)
async def create(game: GameCreateSchema) -> GameDBSchema:
    """
    Creating a new game.
    Return a GameDBScheme with created entity data.
    """
    return GameDBSchema(title="Test game title")


@router.put('/{game_id}/', response_model=GameDBSchema)
async def update(game_id: int) -> GameDBSchema:
    """
    Updates game fields not related to publish/admin functions.
    Returns a GameDBScheme with updated entity data.
    """
    return GameDBSchema(title="Updated test game title")


@router.delete('/{game_id}/')
async def delete(game_id: int) -> Response:
    """
    Removes a game with the specified ID.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/approve/')
async def approve(game_id: int, approving: GameApprovingSchema) -> Response:
    """
    If it denies, the game becomes unpublished and not sent for verification.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/verify/')
async def verify(game_id: int) -> Response:
    """
    Sends a game for verification.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/publish/')
async def publish(game_id: int) -> Response:
    """
    Publishes the game.
    After that, it is shown in the store,
    available for viewing and downloading.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
