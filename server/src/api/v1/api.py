from fastapi import APIRouter

from server.src.core.settings import Tags, API_VERSION_1_PREFIX
from server.src.api.v1.endpoints.auth import router as auth_router
from server.src.api.v1.endpoints.games import router as games_router
from server.src.api.v1.endpoints.companies import router as companies_router
from server.src.api.v1.endpoints.users import router as users_router
from server.src.api.v1.endpoints.library import router as library_router

router = APIRouter(prefix=API_VERSION_1_PREFIX, tags=[Tags.V1])

router.include_router(auth_router)
router.include_router(games_router)
router.include_router(companies_router)
router.include_router(users_router)
router.include_router(library_router)
