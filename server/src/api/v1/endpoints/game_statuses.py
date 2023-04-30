from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.src.api.v1.schemas.language import LanguageCreateSchema
from server.src.core.models.game_status import GameStatus
from server.src.core.models.language import Language
from server.src.core.models.user import User
from server.src.core.settings import Tags, LANGUAGES_ROUTER_PREFIX, GAME_STATUSES_ROUTER_PREFIX
from server.src.core.utils.auth import _get_current_user, GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix=GAME_STATUSES_ROUTER_PREFIX, tags=[Tags.STATUSES])


@router.get('/')
async def items(db: Session = Depends(get_db)):
    return db.query(GameStatus).all()
