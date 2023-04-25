import uuid

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status
from starlette.responses import Response

from server.src.core.controllers.game import GameController
from server.src.core.models.company import Company
from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.models.user import User
from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GameStatusType, GAMES_ASSETS_PATH, \
    GAMES_ASSETS_HEADER_DIR, GAMES_ASSETS_CAPSULE_DIR, GAMES_ASSETS_TRAILERS_DIR, GAMES_ASSETS_SCREENSHOTS_DIR, \
    GAMES_ASSETS_BUILDS_DIR
from server.src.core.utils.auth import get_current_user
from server.src.core.utils.db import get_db
from server.src.schemas.game import GameFilterSchema, GameCreateSchema, GameApprovingSchema, GameSendingSchema, \
    GamePublishingSchema
from server.src.api.v1.endpoints.assets import router as assets_router

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])
router.include_router(assets_router)


@router.get('/')
async def items(game_filter: GameFilterSchema = Body(None),
                db=Depends(get_db)):
    published_status = await GameStatus.by_title(db, GameStatusType.PUBLISHED)

    if game_filter is None:
        game_filter = GameFilterSchema(status_id=[published_status.id])

    if game_filter.status_id is None:
        game_filter.status_id = [published_status.id]

    games = db.query(Game).filter(Game.status_id.in_(game_filter.status_id))

    return games.all()


@router.post('/')
async def create(new_game_data: GameCreateSchema,
                 db=Depends(get_db),
                 current_user: User = Depends(get_current_user)):
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

    not_send_status = await GameStatus.by_title(db, GameStatusType.NOT_SEND)
    game.status_id = not_send_status.id

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


@router.patch('/{game_id}/verify/')
async def verify(game_id: int,
                 sending: GameSendingSchema,
                 db=Depends(get_db)):
    """Sends a game for verification."""

    new_game_status = await GameStatus.by_title(db, GameStatusType.SEND if sending.is_send else GameStatusType.NOT_SEND)

    game = await Game.by_id(db, game_id)

    game.update(db, {"status_id": new_game_status.id})


@router.patch('/{game_id}/approve/')
async def approve(game_id: int,
                  approving: GameApprovingSchema,
                  db=Depends(get_db)):
    """If it denies, the game becomes not sent for verification."""

    new_game_status = await GameStatus.by_title(db, GameStatusType.NOT_PUBLISHED if approving.is_approved else GameStatusType.NOT_SEND)

    game = await Game.by_id(db, game_id)

    game.update(db, {"status_id": new_game_status.id})


@router.patch('/{game_id}/publish/')
async def publish(game_id: int,
                  publishing: GamePublishingSchema,
                  game_controller: GameController = Depends(GameController)) -> Response:
    """
    Publishes the game.
    After that, it is available for downloading.
    """

    await game_controller.manage_publishing(game_id, publishing)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
