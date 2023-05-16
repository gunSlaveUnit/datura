import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from common.api.v1.schemas.notification import NotificationCreateSchema
from server.src.api.v1.endpoints import notifications
from server.src.core.models.company import Company
from server.src.core.models.game import Game
from server.src.core.models.library import Library
from server.src.core.models.user import User
from server.src.core.settings import Tags, GAMES_ROUTER_PREFIX, GAMES_ASSETS_PATH, \
    GAMES_ASSETS_HEADER_DIR, GAMES_ASSETS_CAPSULE_DIR, GAMES_ASSETS_TRAILERS_DIR, GAMES_ASSETS_SCREENSHOTS_DIR, \
    GAMES_ASSETS_BUILDS_DIR, RoleType
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db
from common.api.v1.schemas.game import GameFilterSchema, GameCreateSchema, GameApprovingSchema, GameSendingSchema, \
    GamePublishingSchema, GameDBSchema
from server.src.api.v1.endpoints.assets import router as assets_router
from server.src.api.v1.endpoints.game_tags import router as tags_router
from server.src.api.v1.endpoints.reviews import router as reviews_router

router = APIRouter(prefix=GAMES_ROUTER_PREFIX, tags=[Tags.GAMES])
router.include_router(assets_router)
router.include_router(tags_router)
router.include_router(reviews_router)


@router.get('/')
async def items(filters: GameFilterSchema = Body(None),
                company_id: int = Query(None),
                db=Depends(get_db),
                current_user: User = Depends(GetCurrentUser(is_required=False))):
    games_query = db.query(Game)

    if company_id:
        company = await Company.by_id(db, company_id)
        games_query = games_query.filter(Game.owner_id == company.owner_id)

    if current_user is None or current_user.is_superuser:
        if filters is None:
            filters = GameFilterSchema(is_published=True)
        games_query = games_query.filter(Game.is_published == filters.is_published)
    else:
        games_query = games_query.filter(or_(Game.owner_id == current_user.id, Game.is_published == True))

    return games_query.all()


@router.get('/{game_id}/')
async def item(game_id: int,
               db=Depends(get_db)):
    return await Game.by_id(db, game_id)


@router.post('/', response_model=GameDBSchema)
async def create(new_game_data: GameCreateSchema,
                 db=Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())):
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

    new_directory_uuid = str(uuid.uuid4())
    assets_directory = GAMES_ASSETS_PATH.joinpath(new_directory_uuid)
    assets_directory.mkdir(parents=True)
    assets_directory.joinpath(GAMES_ASSETS_HEADER_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_CAPSULE_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_TRAILERS_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_SCREENSHOTS_DIR).mkdir()
    assets_directory.joinpath(GAMES_ASSETS_BUILDS_DIR).mkdir()
    game.directory = new_directory_uuid

    new_game = await Game.create(db, game)

    new_library_record = Library(
        player_id=current_user.id,
        game_id=new_game.id
    )

    await Library.create(db, new_library_record)

    return new_game


@router.put('/{game_id}/')
async def update(game_id: int,
                 updated_game_data: GameCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())):
    """
    Updates game fields not related to publish/admin functions.
    Returns a GameDBScheme with updated entity data.
    """

    game = await Game.by_id(db, game_id)
    return await game.update(db, updated_game_data.dict())


@router.patch('/{game_id}/approve/')
async def approve(
        game_id: int,
        approving: GameApprovingSchema,
        db: Session = Depends(get_db),
        current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,)))
):
    """
    Update the status of a game based on its approval.

    If the game is denied, it is no longer sent for verification and is not published.
    If the game is approved, it is no longer sent for verification and becomes available for publishing.

    :param game_id: ID of the game to update.
    :param approving: Schema describing the approval of the game.
    :param db: Database session object.

    :return: Updated game object.
    """

    game = await Game.by_id(db, game_id)

    update_dict = {
        "is_approved": approving.is_approved,
        "is_send_for_verification": False
    }
    if not approving.is_approved:
        update_dict["is_published"] = False
    await game.update(db, update_dict)

    if approving.is_approved:
        owner = await User.by_id(db, game.owner_id)
        email_notification_body = f"Уважаемый {owner.account_name}! " \
                                  f"Сведения о Вашем продукте {game.title} были успешно проверены и одобрены. " \
                                  "Вы можете опубликовать его в магазине. " \
                                  "Спасибо, что пользуетесь нашими услугами! С уважением, команда Foggie."
        notification = NotificationCreateSchema(user_id=game.owner_id, content=email_notification_body)
        await notifications.create(notification, db, current_user)

    # Return the updated game object.
    return game


@router.patch('/{game_id}/verify/')
async def verify(game_id: int,
                 sending: GameSendingSchema,
                 db=Depends(get_db)):
    """Sends a game for verification."""

    game = await Game.by_id(db, game_id)

    await game.update(db, {
        "is_approved": False,
        "is_send_for_verification": sending.is_send_for_verification,
        "is_published": False
    })


@router.patch('/{game_id}/publish/')
async def publish(game_id: int,
                  publishing: GamePublishingSchema,
                  db=Depends(get_db)):
    """
    Publishes the game.
    After that, it is available for downloading.
    """

    game = await Game.by_id(db, game_id)

    if not game.is_approved and publishing.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The game cannot be published because it was not approved"
        )

    await game.update(db, {
        "is_send_for_verification": False,
        "is_published": publishing.is_published
    })
