import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, StreamingResponse

from server.src.models.game import Game
from server.src.settings import ASSETS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_CAPSULE_DIR, \
    GAMES_ASSETS_SCREENSHOTS_DIR
from server.src.routes.builds import router as builds_router
from server.src.utils.db import get_db
from server.src.utils.io import read_chunks, CHUNK_SIZE, store

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX)
router.include_router(builds_router)


@router.get('/header/')
async def download_header():
    """
    Returns an image for the header section of the game.
    """
    pass


@router.post('/header/')
async def upload_header(file: UploadFile):
    """
    Uploads a header game section file to the server.
    If exists, won't be overwritten or created on more.
    """
    pass


@router.put('/header/')
async def update_header(file: UploadFile):
    """
    Uploads a header game section file to the server to update existing file.
    If not exists, won't be created.
    If the file is updated, the associated game will become unpublished.
    """
    pass


@router.delete('/header/')
async def delete_header():
    """
    Deletes an existing header game section file.
    If the file is deleted, the associated game will become unpublished.
    """
    pass


@router.get('/capsule/')
async def download_capsule(game_id: int,
                           db: Session = Depends(get_db)):
    """
    Returns an image for the capsule section of the game.
    """

    game = db.query(Game).filter(Game.id == game_id).one()

    capsule_directory = Path(GAMES_ASSETS_PATH)
    capsule_directory = capsule_directory.joinpath(game.directory, GAMES_ASSETS_CAPSULE_DIR)

    # TODO: I don't like this
    capsule_filename = [f for f in os.listdir(capsule_directory) if
                        os.path.isfile(capsule_directory.joinpath(f))][0]

    return FileResponse(capsule_directory.joinpath(capsule_filename))


@router.post('/capsule/')
async def upload_capsule(file: UploadFile):
    """
    Uploads a capsule game section file to the server.
    If exists, won't be overwritten or created on more.
    """
    pass


@router.put('/capsule/')
async def update_capsule(file: UploadFile):
    """
    Uploads a capsule game section file to the server to update existing file.
    If not exists, won't be created.
    If the file is updated, the associated game will become unpublished.
    """
    pass


@router.delete('/capsule/')
async def delete_capsule():
    """
    Deletes an existing capsule game section file.
    If the file is deleted, the associated game will become unpublished.
    """
    pass


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
            read_chunks(path.joinpath(filename), CHUNK_SIZE),
            headers=headers,
            media_type="image/webp"
        )
    else:
        return {"filenames": [f.name for f in path.iterdir() if f.is_file()]}


@router.post('/screenshots/')
async def upload_screenshots(game_id: int,
                             files: List[UploadFile],
                             db: Session = Depends(get_db)):
    """
    Uploads screenshots to the server.
    If something of them exists, won't be overwritten.
    """
    game = db.query(Game).filter(Game.id == game_id).one()

    store_files_directory = Path(GAMES_ASSETS_PATH).joinpath(game.directory, GAMES_ASSETS_SCREENSHOTS_DIR)

    return await store(store_files_directory, files)


@router.put('/screenshots/')
async def update_screenshot(file: UploadFile):
    """
    Uploads a screenshot to the server to update existing file.
    If not exists, won't be created.
    If the file is updated, the associated game will become unpublished.
    """
    pass


@router.delete('/screenshots/')
async def delete_screenshots(filename: str | None = None):
    """
    Deletes an existing screenshot
    or removes all if "filename" query param not provided.
    """
    pass


@router.get('/trailers/')
async def trailers_info(filename: str | None = None):
    """
    Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """
    pass


@router.post('/trailers/')
async def upload_trailers(files: List[UploadFile]):
    """
    Uploads trailers to the server.
    If something of them exists, won't be overwritten.
    """
    pass


@router.put('/trailers/')
async def update_trailer(file: UploadFile):
    """
    Uploads a trailer to the server to update existing file.
    If not exists, won't be created.
    If the file is updated, the associated game will become unpublished.
    """
    pass


@router.delete('/trailer/')
async def delete_trailers(filename: str | None = None):
    """
    Deletes an existing trailer
    or removes all if "filename" query param not provided.
    """
    pass
