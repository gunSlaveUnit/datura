from typing import List

from fastapi import Depends, HTTPException, UploadFile
from starlette import status

from server.src.core.logic.file import FileLogic
from server.src.core.logic.game import GameLogic
from server.src.core.logic.game_status import GameStatusLogic
from server.src.core.settings import GAMES_ASSETS_PATH, GAMES_ASSETS_HEADER_DIR, GameStatusType, \
    GAMES_ASSETS_TRAILERS_DIR
from server.src.core.utils.db import get_db


class AssetsController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.game_logic = GameLogic(db)
        self.game_status_logic = GameStatusLogic(db)

    async def header(self, game_id: int):
        try:
            game = await self.game_logic.item_by_id(game_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game with this id not found"
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

        return await FileLogic.file(searching_directory, files[0].name, "image/webp")

    async def upload_header(self, game_id: int, file: UploadFile):
        try:
            game = await self.game_logic.item_by_id(game_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game with this id not found"
            )

        store_files_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_HEADER_DIR)
        await FileLogic.clear(store_files_directory)

        not_send_status = await self.game_status_logic.item_by_title(GameStatusType.NOT_SEND)
        await self.game_logic.update(game_id, {"status_id": not_send_status.id})

        return await FileLogic.save(store_files_directory, [file])

    async def upload_trailers(self, game_id: int, files: List[UploadFile]):
        try:
            game = await self.game_logic.item_by_id(game_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game with this id not found"
            )

        store_files_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_TRAILERS_DIR)
        await FileLogic.clear(store_files_directory)

        not_send_status = await self.game_status_logic.item_by_title(GameStatusType.NOT_SEND)
        await self.game_logic.update(game_id, {"status_id": not_send_status.id})

        return await FileLogic.save(store_files_directory, files)
