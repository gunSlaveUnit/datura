import json
from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException, Query
from starlette import status
from starlette.responses import Response, FileResponse, StreamingResponse, JSONResponse

from server.src.core.models.game import Game
from server.src.core.models.role import Role
from server.src.core.models.user import User
from server.src.core.settings import ASSETS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_HEADER_DIR, \
    GAMES_ASSETS_TRAILERS_DIR, GAMES_ASSETS_SCREENSHOTS_DIR, GAMES_ASSETS_CAPSULE_DIR, Tags, RoleType
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db
from server.src.core.utils.io import clear, save, read_uncompressed_chunks, CHUNK_SIZE

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX, tags=[Tags.ASSETS])


@router.get('/header/')
async def header_info(game_id: int,
                          db=Depends(get_db),
                          current_user: User | None = Depends(GetCurrentUser(is_required=False))):
    game = await Game.by_id(db, game_id)

    admin_role = await Role.by_title(db, RoleType.ADMIN)

    if not current_user or current_user.role_id != admin_role.id:
        if not game.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset not approved"
            )

    searching_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_HEADER_DIR)

    files = list(searching_directory.glob('*'))

    if files and len(files) != 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Multiple files found but one is required"
        )

    if not files or not files[0].is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return JSONResponse({"filename": files[0].name})


@router.get('/header/file/')
async def download_header(game_id: int,
                          db=Depends(get_db),
                          current_user: User | None = Depends(GetCurrentUser(is_required=False))):
    """Returns an image for the header section of the game."""

    info_response = await header_info(game_id, db, current_user)
    info = json.loads(info_response.body)

    game = await Game.by_id(db, game_id)
    searching_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_HEADER_DIR)

    return FileResponse(
        searching_directory.joinpath(info['filename']),
        headers={"Content-Disposition": f"filename={info['filename']}"},
        media_type="image/webp"
    )


@router.post('/header/')
async def upload_header(game_id: int,
                        file: UploadFile,
                        db=Depends(get_db)):
    """Uploads a header game section file to the server.
    If exists, will be overwritten.
    Associated game will become unpublished.
    """

    game = await Game.by_id(db, game_id)

    store_files_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_HEADER_DIR)
    await clear(store_files_directory)

    await game.update(db, {"is_approved": False})

    await save(store_files_directory, [file])

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/capsule/')
async def download_capsule(game_id: int,
                           db=Depends(get_db),
                           current_user: User | None = Depends(GetCurrentUser(is_required=False))):
    """Returns an image for the capsule section of the game."""

    game = await Game.by_id(db, game_id)

    admin_role = await Role.by_title(db, RoleType.ADMIN)

    if not current_user or current_user.role_id != admin_role.id:
        if not game.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset not approved"
            )

    searching_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_CAPSULE_DIR)

    files = list(searching_directory.glob('*'))

    if files and len(files) != 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Multiple files found but one is required"
        )

    if not files or not files[0].is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileResponse(
        searching_directory.joinpath(files[0].name),
        headers={"Content-Disposition": f"filename={files[0].name}"},
        media_type="image/webp"
    )


@router.post('/capsule/')
async def upload_capsule(game_id: int,
                         file: UploadFile,
                         db=Depends(get_db)):
    """Uploads a capsule game section file to the server.
    If exists, will be overwritten.
    Associated game will become unpublished.
    """

    game = await Game.by_id(db, game_id)

    store_files_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_CAPSULE_DIR)
    await clear(store_files_directory)

    await game.update(db, {"is_approved": False})

    await save(store_files_directory, [file])

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/screenshots/')
async def screenshots_info(game_id: int,
                           db=Depends(get_db),
                           filename: str = Query(None),
                           current_user: User | None = Depends(GetCurrentUser(is_required=False))):
    """Returns the names of the screenshot files.
    If "filename" query param was provided, returns a file.
    """

    game = await Game.by_id(db, game_id)

    admin_role = await Role.by_title(db, RoleType.ADMIN)

    if not current_user or current_user.role_id != admin_role.id:
        if not game.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset not approved"
            )

    path = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_SCREENSHOTS_DIR)

    if filename:
        headers = {"Content-Disposition": f"filename={filename}"}

        return StreamingResponse(
            read_uncompressed_chunks(path.joinpath(filename), CHUNK_SIZE),
            headers=headers,
            media_type="image/webp"
        )
    else:
        return {"filenames": [f.name for f in path.iterdir() if f.is_file()]}


@router.post('/screenshots/')
async def upload_screenshots(game_id: int,
                             files: List[UploadFile],
                             db=Depends(get_db)):
    """Uploads screenshots to the server.
    All will be overwritten.
    Associated game will become unpublished.
    """

    game = await Game.by_id(db, game_id)

    store_files_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_SCREENSHOTS_DIR)
    await clear(store_files_directory)

    await game.update(db, {"is_approved": False})

    await save(store_files_directory, files)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/trailers/')
async def trailers_info(game_id: int,
                        db=Depends(get_db),
                        filename: str = Query(None),
                        current_user: User | None = Depends(GetCurrentUser(is_required=False))):
    """Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """

    game = await Game.by_id(db, game_id)

    admin_role = await Role.by_title(db, RoleType.ADMIN)

    if not current_user or current_user.role_id != admin_role.id:
        if not game.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset not approved"
            )

    path = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_TRAILERS_DIR)

    if filename:
        headers = {"Content-Disposition": f"filename={filename}"}

        return StreamingResponse(
            read_uncompressed_chunks(path.joinpath(filename), CHUNK_SIZE),
            headers=headers,
            media_type="video/webm"
        )
    else:
        return {"filenames": [f.name for f in path.iterdir() if f.is_file()]}


@router.post('/trailers/')
async def upload_trailers(game_id: int,
                          files: List[UploadFile],
                          db=Depends(get_db)):
    """Uploads trailers to the server.
    All will be overwritten.
    Associated game will become unpublished.
    """

    game = await Game.by_id(db, game_id)

    store_files_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_TRAILERS_DIR)
    await clear(store_files_directory)

    await game.update(db, {"is_approved": False})

    await save(store_files_directory, files)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
