from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import ADMIN_ROUTER_PREFIX, Tags, templates, RoleType
from server.oldsrc.admin.endpoints.login import router as login_router
from server.oldsrc.admin.endpoints.companies import router as companies_router
from server.oldsrc.admin.endpoints.games import router as games_router
from server.oldsrc.core.utils.auth import GetCurrentUser

router = APIRouter(prefix=ADMIN_ROUTER_PREFIX, tags=[Tags.ADMIN])
router.include_router(login_router)
router.include_router(companies_router)
router.include_router(games_router)


@router.get('/', response_class=HTMLResponse)
async def home(request: Request,
               current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,)))):
    return templates.TemplateResponse("home.html", {"request": request})
