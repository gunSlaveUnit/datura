from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException, Query
from starlette import status
from starlette.responses import Response, FileResponse, StreamingResponse

from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.settings import ASSETS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_HEADER_DIR, GameStatusType, \
    GAMES_ASSETS_TRAILERS_DIR, GAMES_ASSETS_SCREENSHOTS_DIR, GAMES_ASSETS_CAPSULE_DIR, Tags
from server.src.core.utils.db import get_db
from server.src.core.utils.io import clear, save, read_uncompressed_chunks, CHUNK_SIZE
from server.src.api.v1.endpoints.builds import router as builds_router


router = APIRouter(prefix=ASSETS_ROUTER_PREFIX, tags=[Tags.ASSETS])
router.include_router(builds_router)


@router.get('/header/')
async def download_header(game_id: int,
                          db=Depends(get_db)):
    """Returns an image for the header section of the game."""

    game = await Game.by_id(db, game_id)

    part_published_status = await GameStatus.by_title(db, GameStatusType.PART_PUBLISHED)
    full_published_status = await GameStatus.by_title(db, GameStatusType.FULL_PUBLISHED)
    if game.status_id not in [part_published_status, full_published_status]:
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

    return FileResponse(
        searching_directory.joinpath(files[0].name),
        headers={"Content-Disposition": f"filename={files[0].name}"},
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

    not_send_status = await GameStatus.by_title(db, GameStatusType.NOT_SEND)
    game.update(db, {"status_id": not_send_status.id})

    await save(store_files_directory, [file])

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/capsule/')
async def download_capsule(game_id: int,
                           db=Depends(get_db)):
    """Returns an image for the capsule section of the game."""

    game = await Game.by_id(db, game_id)

    part_published_status = await GameStatus.by_title(db, GameStatusType.PART_PUBLISHED)
    full_published_status = await GameStatus.by_title(db, GameStatusType.FULL_PUBLISHED)
    if game.status_id not in [part_published_status, full_published_status]:
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

    not_send_status = await GameStatus.by_title(db, GameStatusType.NOT_SEND)
    await game.update(db, {"status_id": not_send_status.id})

    await save(store_files_directory, [file])

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/screenshots/')
async def screenshots_info(game_id: int,
                           db=Depends(get_db),
                           filename: str = Query(None)):
    """Returns the names of the screenshot files.
    If "filename" query param was provided, returns a file.
    """

    game = await Game.by_id(db, game_id)

    part_published_status = await GameStatus.by_title(db, GameStatusType.PART_PUBLISHED)
    full_published_status = await GameStatus.by_title(db, GameStatusType.FULL_PUBLISHED)
    if game.status_id not in [part_published_status, full_published_status]:
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

    not_send_status = await GameStatus.by_title(db, GameStatusType.NOT_SEND)
    game.update(db, {"status_id": not_send_status.id})

    await save(store_files_directory, files)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/trailers/')
async def trailers_info(game_id: int,
                        db=Depends(get_db),
                        filename: str = Query(None)):
    """Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """

    game = await Game.by_id(db, game_id)

    part_published_status = await GameStatus.by_title(db, GameStatusType.PART_PUBLISHED)
    full_published_status = await GameStatus.by_title(db, GameStatusType.FULL_PUBLISHED)
    if game.status_id not in [part_published_status, full_published_status]:
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

    not_send_status = await GameStatus.by_title(db, GameStatusType.NOT_SEND)
    game.update(db, {"status_id": not_send_status.id})

    await save(store_files_directory, files)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
