from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.core.models.user import User
from server.src.core.settings import templates, RoleType
from server.src.core.utils.auth import GetCurrentUser

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
