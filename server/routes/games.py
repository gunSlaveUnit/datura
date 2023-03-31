from fastapi import APIRouter

from settings import GAMES_ROUTER_PREFIX, Tags

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])


@router.get('/')
def list_all():
    return {"message": "test"}
