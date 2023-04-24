from typing import List

from fastapi import APIRouter, UploadFile, Depends
from starlette import status
from starlette.responses import Response

from server.src.core.controllers.assets import AssetsController
from server.src.core.settings import ASSETS_ROUTER_PREFIX, GAMES_ASSETS_HEADER_DIR

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX)


@router.get('/header/')
async def download_header(game_id: int,
                          assets_controller: AssetsController = Depends(AssetsController)):
    """Returns an image for the header section of the game."""

    return await assets_controller.header(game_id)


@router.post('/header/')
async def upload_header(game_id: int,
                        file: UploadFile,
                        assets_controller: AssetsController = Depends(AssetsController)):
    """Uploads a header game section file to the server.
    If exists, will be overwritten.
    Associated game will become unpublished.
    """

    await assets_controller.upload_header(game_id, file)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/capsule/')
async def download_capsule(game_id: int):
    """Returns an image for the capsule section of the game."""

    pass


@router.post('/capsule/')
async def upload_capsule(file: UploadFile):
    """Uploads a capsule game section file to the server.
    If exists, will be overwritten.
    Associated game will become unpublished.
    """

    pass


@router.get('/screenshots/')
async def screenshots_info(game_id: int):
    """Returns the names of the screenshot files.
    If "filename" query param was provided, returns a file.
    """

    pass


@router.post('/screenshots/')
async def upload_screenshots(game_id: int):
    """Uploads screenshots to the server.
    All will be overwritten.
    Associated game will become unpublished.
    """

    pass


@router.get('/trailers/')
async def trailers_info(filename: str | None = None):
    """Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """
    pass


@router.post('/trailers/')
async def upload_trailers(files: List[UploadFile]):
    """Uploads trailers to the server.
    All will be overwritten.
    Associated game will become unpublished.
    """

    pass
