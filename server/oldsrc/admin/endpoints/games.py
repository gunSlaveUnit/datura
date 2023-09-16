import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.oldsrc.api.v1.endpoints import games
from server.oldsrc.core.models.build import Build
from server.oldsrc.core.models.game import Game
from server.oldsrc.core.models.platform import Platform
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import RoleType, templates
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

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
    builds_query = db.query(Build).filter(Build.game_id == game_id)

    builds_query = builds_query.join(Platform)
    builds_query = builds_query.options(joinedload(Build.platform))

    game = await games.item(game_id, db)
    game.release_date = datetime.datetime.fromtimestamp(game.release_date).strftime("%d.%m.%Y")

    return templates.TemplateResponse("detailed_game.html", {
        "request": request,
        "game": game,
        "builds": builds_query.all()
    })
