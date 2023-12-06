from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.core.settings import templates

router = APIRouter()


@router.get('/login/', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
