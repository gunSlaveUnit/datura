from typing import List

from fastapi import APIRouter, UploadFile

from settings import ASSETS_ROUTER_PREFIX, Tags

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX, tags=[Tags.GAMES])


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
async def download_capsule():
    """
    Returns an image for the capsule section of the game.
    """
    pass


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
async def screenshots_info(filename: str | None = None):
    """
    Returns the names of the screenshot files.
    If "filename" query param was provided, returns a file.
    """
    pass


@router.post('/screenshots/')
async def upload_screenshots(files: List[UploadFile]):
    """
    Uploads screenshots to the server.
    If something of them exists, won't be overwritten.
    """
    pass


@router.put('/screenshots/')
async def update_screenshot(file: UploadFile):
    """
    Uploads a screenshot to the server to update existing file.
    If not exists, won't be created.
    If the file is updated, the associated game will become unpublished.
    """
    pass


@router.delete('/screenshots/')
async def delete_screenshot(filename: str):
    """
    Deletes an existing screenshot.
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


@router.get('/build/')
async def build_info(filename: str | None = None):
    """
    Returns the names of the build files.
    If "filename" query param was provided, returns a file.
    """
    pass
