from fastapi import APIRouter

from server.src.core.settings import ADMIN_ROUTER_PREFIX, Tags
from server.src.admin.endpoints.home import router as home_router

router = APIRouter(prefix=ADMIN_ROUTER_PREFIX, tags=[Tags.ADMIN])
router.include_router(home_router)
