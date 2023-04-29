from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.core.settings import ADMIN_ROUTER_PREFIX, Tags, templates
from server.src.admin.endpoints.login import router as login_router

router = APIRouter(prefix=ADMIN_ROUTER_PREFIX, tags=[Tags.ADMIN])
router.include_router(login_router)


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
