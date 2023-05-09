import asyncio
import concurrent
import gzip
import hashlib
import io
import uuid
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import aiofiles
from fastapi import APIRouter, UploadFile, Depends, Query, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response

from common.api.v1.schemas.build import BuildDBSchema, BuildCreateSchema
from server.src.core.models.build import Build
from server.src.core.models.game import Game
from server.src.core.models.platform import Platform
from server.src.core.models.user import User
from server.src.core.settings import BUILDS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_BUILDS_DIR, Tags
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db
from server.src.core.utils.io import MEDIA_TYPE, read_compressed_chunks, CHUNK_SIZE, clear, read_uncompressed_chunks

router = APIRouter(prefix=BUILDS_ROUTER_PREFIX, tags=[Tags.BUILDS])


@router.get('/')
async def items(game_id: int = Query(None),
                include_platform: bool = False,
                db: Session = Depends(get_db)):
    items_query = db.query(Build)

    if game_id:
        items_query = items_query.filter(Build.game_id == game_id)

    if include_platform:
        items_query = items_query.join(Platform)
        items_query = items_query.options(joinedload(Build.platform))

    return items_query.all()


@router.get('/{build_id}/')
async def item(build_id: int,
               db: Session = Depends(get_db)):
    return await Build.by_id(db, build_id)


@router.post('/', response_model=BuildDBSchema)
async def create(build_create_data: BuildCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())) -> BuildDBSchema:
    """
    Creating a new build for specified game.
    Return a BuildDBSchema with created entity data.
    """

    game = await Game.by_id(db, build_create_data.game_id)
    if game.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not the owner of this game"
        )

    build = Build(**vars(build_create_data))

    related_game_directory = game.directory

    new_directory_uuid = str(uuid.uuid4())
    build_directory = GAMES_ASSETS_PATH.joinpath(related_game_directory, GAMES_ASSETS_BUILDS_DIR, new_directory_uuid)
    build_directory.mkdir(parents=True)
    build.directory = new_directory_uuid

    await Build.create(db, build)
    await game.update(db, {"is_approved": False, "is_published": False})

    return build


@router.put('/{build_id}/', response_model=BuildDBSchema)
async def update(build_id: int,
                 build_updated_data: BuildCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())) -> BuildDBSchema:
    game = await Game.by_id(db, build_updated_data.game_id)

    if game.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not the owner of this game"
        )

    build = await Build.by_id(db, build_id)

    return await build.update(db, build_updated_data.dict())


def get_file_info(filepath: Path, base_path: Path):
    sha1 = hashlib.sha1()

    for chunk in read_uncompressed_chunks(filepath):
        sha1.update(chunk)

    return {
        "sha-1": sha1.hexdigest(),
        "size_bytes": filepath.stat().st_size,
        'rel_path': filepath.relative_to(base_path)
    }


async def files_info(path: Path):
    futures = []
    pool = ThreadPoolExecutor(8)
    loop = asyncio.get_running_loop()
    for file_path in path.glob("**/*"):
        if file_path.is_file():
            futures.append(loop.run_in_executor(pool, get_file_info, file_path, path))

    await asyncio.gather(*futures)

    files = []
    for future in futures:
        files.append(future.result())

    return {"files": files}


@router.get('/{build_id}/files/')
async def build_info(build_id: int,
                     filename: str | None = None,
                     db: Session = Depends(get_db)):
    """
    Returns the names of the build files.
    If "filename" query param was provided, returns a file.
    """

    build = await Build.by_id(db, build_id)
    game = await Game.by_id(db, build.game_id)

    path = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_BUILDS_DIR, build.directory)

    if filename:
        return StreamingResponse(
            read_compressed_chunks(path.joinpath(filename), CHUNK_SIZE),
            media_type=MEDIA_TYPE
        )
    else:
        return await files_info(path)


@router.post('/{build_id}/files/')
async def upload_build(build_id: int,
                       request: Request,
                       content_disposition: str = Header(),
                       db: Session = Depends(get_db)):
    """
    Uploads project build files to the server.
    All will be overwritten.
    """
    build = await Build.by_id(db, build_id)
    game = await Game.by_id(db, build.game_id)

    store_files_directory = Path(GAMES_ASSETS_PATH).joinpath(game.directory, GAMES_ASSETS_BUILDS_DIR, build.directory)

    possible_directory = store_files_directory.joinpath(content_disposition).parent

    if not possible_directory.exists():
        possible_directory.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(store_files_directory.joinpath(content_disposition), 'ab') as f:
        body_bytes = await request.body()
        await f.write(body_bytes)
