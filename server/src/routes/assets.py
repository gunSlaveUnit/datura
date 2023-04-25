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



@router.get('/screenshots/')
async def screenshots_info(game_id: int,
                           db: Session = Depends(get_db),
                           filename: str | None = None):
    """
    Returns the names of the screenshot files.
    If "filename" query param was provided, returns a file.
    """
    game = db.query(Game).filter(Game.id == game_id).one()

    path = Path(GAMES_ASSETS_PATH).joinpath(game.directory, GAMES_ASSETS_SCREENSHOTS_DIR)

    if filename:
        headers = {"Content-Disposition": f"filename={filename}"}

        return StreamingResponse(
            read_uncompressed_chunks(path.joinpath(filename), CHUNK_SIZE),
            headers=headers,
            media_type="image/webp"
        )
    else:
        return {"filenames": [f.name for f in path.iterdir() if f.is_file()]}


@router.get('/trailers/')
async def trailers_info(filename: str | None = None):
    """
    Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """
    pass
