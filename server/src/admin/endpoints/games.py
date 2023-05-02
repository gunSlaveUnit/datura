from pprint import pprint

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.api.v1.endpoints import games
from server.src.core.models.game import Game
from server.src.core.models.user import User
from server.src.core.settings import RoleType, templates
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix='/games')


@router.get('/', response_class=HTMLResponse)
async def items(request: Request,
                current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,))),
                db: Session = Depends(get_db)):

    games_query = db.query(Game).order_by(Game.is_send_for_verification, desc(Game.created_at))

    return templates.TemplateResponse("games.html", {"request": request, "games": games_query.all()})


@router.get('/{game_id}/', response_class=HTMLResponse)
async def item(request: Request,
               game_id: int,
               db: Session = Depends(get_db),
               _: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,)))):
    return templates.TemplateResponse("detailed_game.html", {
        "request": request,
        "game": await games.item(game_id, db)
    })
