from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from schemes.games import GameCreateScheme, GameDBScheme
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
