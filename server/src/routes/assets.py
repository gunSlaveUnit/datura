import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, StreamingResponse

from server.src.core.models import Game
from server.src.core.settings import ASSETS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_CAPSULE_DIR, \
    GAMES_ASSETS_SCREENSHOTS_DIR
from server.src.routes.builds import router as builds_router
from server.src.core.utils import get_db
from server.src.core.utils.io import CHUNK_SIZE, store, read_uncompressed_chunks

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX)
router.include_router(builds_router)




@router.get('/trailers/')
async def trailers_info(filename: str | None = None):
    """
    Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """
    pass
