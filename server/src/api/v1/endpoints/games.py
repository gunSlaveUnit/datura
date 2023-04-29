import uuid

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from server.src.core.models.company import Company
from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.models.user import User
from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GameStatusType, GAMES_ASSETS_PATH, \
    GAMES_ASSETS_HEADER_DIR, GAMES_ASSETS_CAPSULE_DIR, GAMES_ASSETS_TRAILERS_DIR, GAMES_ASSETS_SCREENSHOTS_DIR, \
    GAMES_ASSETS_BUILDS_DIR
from server.src.core.utils.auth import _get_current_user, GetCurrentUser
from server.src.core.utils.db import get_db
from server.src.api.v1.schemas.game import GameFilterSchema, GameCreateSchema, GameApprovingSchema, GameSendingSchema, \
    GamePublishingSchema
from server.src.api.v1.endpoints.assets import router as assets_router
from server.src.api.v1.endpoints.game_tags import router as tags_router
from server.src.api.v1.endpoints.reviews import router as reviews_router

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])
router.include_router(assets_router)
router.include_router(tags_router)
router.include_router(reviews_router)


@router.get('/')
async def items(_: GameFilterSchema = Body(None),
                db=Depends(get_db)):
    return db.query(Game).all()


@router.get('/{game_id}/')
async def item(game_id: int,
               db=Depends(get_db)):
    return await Game.by_id(db, game_id)


@router.post('/')
async def create(new_game_data: GameCreateSchema,
                 db=Depends(get_db),
                 current_user: User = Depends(GetCurrentUser)):
    potentially_not_existing_company = await Company.by_owner(db, current_user.id)

    if potentially_not_existing_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Current user does not have a registered company"
        )

    if not potentially_not_existing_company.is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Information about the user's company may be inaccurate. Creating is temporarily disabled"
        )

    game = Game(**vars(new_game_data))
    game.owner_id = current_user.id

    not_approved_status = await GameStatus.by_title(db, GameStatusType.NOT_APPROVED)
    game.status_id = not_approved_status.id

    new_directory_uuid = str(uuid.uuid4())
    assets_directory = GAMES_ASSETS_PATH.joinpath(new_directory_uuid)
    assets_directory.mkdir(parents=True)
    assets_directory.joinpath(GAMES_ASSETS_HEADER_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_CAPSULE_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_TRAILERS_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_SCREENSHOTS_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_BUILDS_DIR).mkdir()
    game.directory = new_directory_uuid

    return await Game.create(db, game)


@router.put('/{game_id}/')
async def update(game_id: int,
                 updated_game_data: GameCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser)):
    """
    Updates game fields not related to publish/admin functions.
    Returns a GameDBScheme with updated entity data.
    """

    game = await Game.by_id(db, game_id)
    return await game.update(db, **vars(updated_game_data))


@router.patch('/{game_id}/verify/')
async def verify(game_id: int,
                 sending: GameSendingSchema,
                 db=Depends(get_db)):
    """Sends a game for verification."""

    new_game_status = await GameStatus.by_title(
        db,
        GameStatusType.SEND if sending.is_send else GameStatusType.NOT_SEND
    )

    game = await Game.by_id(db, game_id)

    await game.update(db, {"status_id": new_game_status.id})


@router.patch('/{game_id}/approve/')
async def approve(game_id: int,
                  approving: GameApprovingSchema,
                  db=Depends(get_db)):
    """If it denies, the game becomes not sent for verification."""

    new_game_status = await GameStatus.by_title(
        db,
        GameStatusType.NOT_PUBLISHED if approving.is_approved else GameStatusType.NOT_SEND
    )

    game = await Game.by_id(db, game_id)

    await game.update(db, {"status_id": new_game_status.id})


@router.patch('/{game_id}/publish/')
async def publish(game_id: int,
                  publishing: GamePublishingSchema,
                  db=Depends(get_db)):
    """
    Publishes the game.
    After that, it is available for downloading.
    """

    game = await Game.by_id(db, game_id)

    not_published_status = await GameStatus.by_title(db, GameStatusType.NOT_PUBLISHED)

    if game.status_id != not_published_status.id and publishing.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The game cannot be published because it was not previously published or was not previously "
                   "submitted for review"
        )

    new_game_status = await GameStatus.by_title(
        db,
        GameStatusType.PUBLISHED if publishing.is_published else GameStatusType.NOT_PUBLISHED
    )

    await game.update(db, {"status_id": new_game_status.id})
