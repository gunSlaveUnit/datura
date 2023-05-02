from fastapi import APIRouter

from server.src.core.settings import Tags, API_VERSION_1_PREFIX
from server.src.api.v1.endpoints.auth import router as auth_router
from server.src.api.v1.endpoints.games import router as games_router
from server.src.api.v1.endpoints.languages import router as languages_router
from server.src.api.v1.endpoints.tags import router as tags_router
from server.src.api.v1.endpoints.companies import router as companies_router
from server.src.api.v1.endpoints.users import router as age_categories_router
from server.src.api.v1.endpoints.platforms import router as platforms_router
from server.src.api.v1.endpoints.age_caterogies import router as users_router
from server.src.api.v1.endpoints.library import router as library_router
from server.src.api.v1.endpoints.cart import router as cart_router
from server.src.api.v1.endpoints.builds import router as builds_router
from server.src.api.v1.endpoints.requirements import router as requirements_router

router = APIRouter(prefix=API_VERSION_1_PREFIX, tags=[Tags.V1])

router.include_router(auth_router)
router.include_router(games_router)
router.include_router(languages_router)
router.include_router(tags_router)
router.include_router(companies_router)
router.include_router(users_router)
router.include_router(age_categories_router)
router.include_router(platforms_router)
router.include_router(library_router)
router.include_router(cart_router)
router.include_router(builds_router)
router.include_router(requirements_router)
