from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from schemes.games import GameCreateScheme, GameDBScheme, GameApprovingScheme
from settings import GAMES_ROUTER_PREFIX, Tags

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])


@router.get('/', response_model=List[GameDBScheme])
async def every() -> List[GameDBScheme]:
    """
    List of all games according to the given filters.
    Returns a list of GameDBScheme with game data.
    """

    return [
        GameDBScheme(title="Test game title 1"),
        GameDBScheme(title="Test game title 2"),
    ]


@router.post('/', response_model=GameDBScheme)
async def create(game: GameCreateScheme) -> GameDBScheme:
    """
    Creating a new game.
    Return a GameDBScheme with created entity data.
    """
    return GameDBScheme(title="Test game title")


@router.put('/{game_id}/', response_model=GameDBScheme)
async def update(game_id: int) -> GameDBScheme:
    """
    Updates game fields not related to publish/admin functions.
    Returns a GameDBScheme with updated entity data.
    """
    return GameDBScheme(title="Updated test game title")


@router.delete('/{game_id}/')
async def delete(game_id: int) -> Response:
    """
    Removes a game with the specified ID.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/approve/')
async def approve(game_id: int, approving: GameApprovingScheme) -> Response:
    """
    If it denies, the game becomes unpublished and not sent for verification
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/verify/')
async def verify(game_id: int) -> Response:
    """
    Sends a game for verification
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
