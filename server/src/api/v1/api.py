from fastapi import APIRouter

from server.src.core.settings import Tags, API_VERSION_1_PREFIX
from server.src.api.v1.endpoints.auth import router as auth_router

router = APIRouter(prefix=API_VERSION_1_PREFIX, tags=[Tags.V1])

router.include_router(auth_router)
