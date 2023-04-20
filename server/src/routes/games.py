import uuid
from pathlib import Path
from typing import List, Type

from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from server.src.models.company import Company
from server.src.models.game import Game
from server.src.models.user import User
from server.src.schemas.game import GameCreateSchema, GameDBSchema, GameApprovingSchema
from server.src.settings import GAMES_ROUTER_PREFIX, Tags, GAMES_ASSETS_PATH, GameStatusType
from server.src.routes.assets import router as assets_router
from server.src.utils.auth import get_current_user
from server.src.utils.db import get_db

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])
router.include_router(assets_router)


@router.get('/', response_model=List[GameDBSchema])
async def every(company_id: int | None = None,
                db: Session = Depends(get_db)) -> list[Type[Game]]:
    """
    List of all games according to the given filters.
    Returns a list of GameDBScheme with game data.
    """

    games = db.query(Game)
    if company_id:
        games = games.filter(Game.company_id == company_id)
    return games.all()


@router.get('/{game_id}/', response_model=GameDBSchema)
async def instance(game_id: int,
                   db: Session = Depends(get_db)) -> Type[Game]:
    """
    List of all games according to the given filters.
    Returns a list of GameDBScheme with game data.
    """

    return db.query(Game).filter(Game.id == game_id).one()


@router.post('/', response_model=GameDBSchema)
async def create(game_create_data: GameCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)) -> GameDBSchema:
    """
    Creating a new game.
    Return a GameDBScheme with created entity data.
    """

    game = Game(**vars(game_create_data))
    game.company = current_user.company
    game.status_id = 1 # TODO: make like a query to NOT_SEND

    assets_directory = Path(GAMES_ASSETS_PATH)
    new_directory_uuid = str(uuid.uuid4())
    assets_directory = assets_directory.joinpath(new_directory_uuid)
    assets_directory.mkdir(parents=True)
    game.directory = new_directory_uuid

    db.add(game)
    db.commit()
    db.refresh(game)

    return game


@router.put('/{game_id}/', response_model=GameDBSchema)
async def update(game_id: int,
                 updated_game_data: GameCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)) -> Type[Game]:
    """
    Updates game fields not related to publish/admin functions.
    Returns a GameDBScheme with updated entity data.
    """

    current_company = db.query(Company).filter(Company.owner_id == current_user.id).one()
    if current_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Current user does not have a registered company"
        )

    updated_game_query = db.query(Game).filter(and_(Game.company_id == current_company.id, Game.id == game_id))
    updated_game = updated_game_query.one()

    if updated_game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no game with this id"
        )

    new_game_data = Game(**vars(updated_game_data))

    updated_game_query.update(new_game_data.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_game)

    return updated_game


@router.delete('/{game_id}/')
async def delete(game_id: int) -> Response:
    """
    Removes a game with the specified ID.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/approve/')
async def approve(game_id: int, approving: GameApprovingSchema) -> Response:
    """
    If it denies, the game becomes unpublished and not sent for verification.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/verify/')
async def verify(game_id: int) -> Response:
    """
    Sends a game for verification.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{game_id}/publish/')
async def publish(game_id: int) -> Response:
    """
    Publishes the game.
    After that, it is shown in the store,
    available for viewing and downloading.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
