import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.responses import StreamingResponse

from server.src.api.v1.schemas.build import BuildDBSchema, BuildCreateSchema
from server.src.core.models.build import Build
from server.src.core.models.game import Game
from server.src.core.models.platform import Platform
from server.src.core.models.user import User
from server.src.core.settings import BUILDS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_BUILDS_DIR, Tags
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db
from server.src.core.utils.io import MEDIA_TYPE, read_compressed_chunks, CHUNK_SIZE, save, clear

router = APIRouter(prefix=BUILDS_ROUTER_PREFIX, tags=[Tags.BUILDS])


@router.get('/', response_model=List[BuildDBSchema])
async def items(game_id: int = Query(None),
                include_platforms: bool = False,
                db: Session = Depends(get_db)):
    items_query = db.query(Build)

    if game_id:
        items_query = items_query.filter(Build.game_id == game_id)

    if include_platforms:
        items_query = items_query.join(Platform)
        items_query = items_query.options(joinedload(Build.platform))

    return items_query.all()


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

    return build


@router.get('/{build_id}/')
async def build_info(game_id: int,
                     build_id: int,
                     filename: str | None = None,
                     db: Session = Depends(get_db)):
    """
    Returns the names of the build files.
    If "filename" query param was provided, returns a file.
    """

    game = await Game.by_id(db, game_id)
    build = await Build.by_id(db, build_id)

    path = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_BUILDS_DIR, build.directory)

    if filename:
        headers = {"Content-Disposition": f"filename={filename}"}

        return StreamingResponse(
            read_compressed_chunks(path.joinpath(filename), CHUNK_SIZE),
            headers=headers,
            media_type=MEDIA_TYPE
        )
    else:
        return {"filenames": [f.name for f in path.iterdir() if f.is_file()]}


@router.post('/{build_id}/')
async def upload_build(game_id: int,
                       build_id: int,
                       files: List[UploadFile],
                       db: Session = Depends(get_db)):
    """
    Uploads project build files to the server.
    All will be overwritten.
    """

    game = await Game.by_id(db, game_id)
    build = await Build.by_id(db, build_id)

    store_files_directory = Path(GAMES_ASSETS_PATH).joinpath(game.directory, GAMES_ASSETS_BUILDS_DIR, build.directory)
    await clear(store_files_directory)

    return await save(store_files_directory, files)
