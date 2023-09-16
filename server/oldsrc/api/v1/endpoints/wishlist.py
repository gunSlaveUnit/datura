from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from common.api.v1.schemas.wishlist import WishlistCreateSchema
from server.oldsrc.core.models.user import User
from server.oldsrc.core.models.wishlist import Wishlist
from server.oldsrc.core.settings import Tags, WISHLIST_ROUTER_PREFIX
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=WISHLIST_ROUTER_PREFIX, tags=[Tags.WISHLIST])


@router.get('/')
async def items(user_id: int | None = None,
                game_id: int | None = None,
                include_games: bool = False,
                db: Session = Depends(get_db),
                _: User = Depends(GetCurrentUser(is_required=False))):
    records_query = db.query(Wishlist)

    if user_id:
        records_query = records_query.filter(Wishlist.user_id == user_id)

    if game_id:
        records_query = records_query.filter(Wishlist.game_id == game_id)

    if include_games:
        records_query = records_query.options(joinedload(Wishlist.game))

    return records_query.all()


@router.post('/')
async def create(new_wishlist_record: WishlistCreateSchema,
                 db: Session = Depends(get_db),
                 _: User = Depends(GetCurrentUser())):
    wishlist_record = Wishlist(**vars(new_wishlist_record))
    return await Wishlist.create(db, wishlist_record)
