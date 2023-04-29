from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.core.settings import templates

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
