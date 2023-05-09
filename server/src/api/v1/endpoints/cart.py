from typing import Type

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.responses import Response

from common.api.v1.schemas.cart import CartDBSchema, CartCreateSchema
from server.src.core.models.cart import Cart
from server.src.core.models.game import Game
from server.src.core.models.library import Library
from server.src.core.models.user import User
from server.src.core.settings import CART_ROUTER_PREFIX, Tags
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix=CART_ROUTER_PREFIX, tags=[Tags.CART])


@router.get('/')
async def items(db: Session = Depends(get_db),
                include_games: bool = Query(None),
                current_user: User = Depends(GetCurrentUser())):
    items_query = db.query(Cart).filter(Cart.buyer_id == current_user.id)

    if include_games:
        items_query = items_query.options(joinedload(Cart.game))

    return items_query.all()


@router.post('/', response_model=CartDBSchema)
async def create(new_record: CartCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())) -> Type[Cart]:
    record = Cart(**vars(new_record))
    record.buyer_id = current_user.id

    return await Cart.create(db, record)


@router.post('/pay/')
async def pay(db: Session = Depends(get_db),
              current_user: User = Depends(GetCurrentUser())):
    items = db.query(Cart).filter(Cart.buyer_id == current_user.id).all()

    for record in items:
        new_library_record = Library(
            player_id=current_user.id,
            game_id=record.game_id
        )

        await Library.create(db, new_library_record)
        await Cart.delete(db, record.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
