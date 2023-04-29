from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.core.models.user import User
from server.src.core.settings import ADMIN_ROUTER_PREFIX, Tags, templates, RoleType
from server.src.admin.endpoints.login import router as login_router
from server.src.core.utils.auth import GetCurrentUser

router = APIRouter(prefix=ADMIN_ROUTER_PREFIX, tags=[Tags.ADMIN])
router.include_router(login_router)


@router.get('/', response_class=HTMLResponse)
async def home(request: Request,
               current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,)))):
    return templates.TemplateResponse("home.html", {"request": request})
