from typing import List

from fastapi import APIRouter, UploadFile

from server.src.settings import BUILDS_ROUTER_PREFIX

router = APIRouter(prefix=BUILDS_ROUTER_PREFIX)


@router.get('/')
async def every():
    pass


@router.post('/')
async def create():
    pass


@router.put('/{build_id}/')
async def update(build_id: int):
    pass


@router.delete('/{build_id}/')
async def delete(build_id: int):
    pass


@router.get('/{build_id}/')
async def build_info(filename: str | None = None):
    """
    Returns the names of the build files.
    If "filename" query param was provided, returns a file.
    """
    pass


@router.post('/{build_id}/')
async def upload_build(files: List[UploadFile]):
    """
    Uploads project build files to the server.
    If something of them exists, won't be overwritten.
    """
    pass


@router.put('/{build_id}/')
async def update_build(file: UploadFile):
    """
    Uploads a build file to the server to update existing file.
    If not exists, won't be created.
    If the file is updated, the associated game will become unpublished.
    """
    pass


@router.delete('/{build_id}/')
async def delete_build(filename: str | None = None):
    """
    Deletes an existing build file
    or removes all if "filename" query param not provided.
    """
    pass
