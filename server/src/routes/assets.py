from fastapi import APIRouter

from settings import ASSETS_ROUTER_PREFIX, Tags

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX, tags=[Tags.GAMES])


@router.get('/header/')
async def download_header():
    """
    Returns an image for the header section of the game
    """
    pass
