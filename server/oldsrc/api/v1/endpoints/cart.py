import json
from typing import Type

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.responses import Response

from common.api.v1.schemas.cart import CartDBSchema, CartCreateSchema
from server.oldsrc.api.v1.endpoints.users import balance
from server.oldsrc.core.models.cart import Cart
from server.oldsrc.core.models.game import Game
from server.oldsrc.core.models.library import Library
from server.oldsrc.core.models.purchase import Purchase
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import CART_ROUTER_PREFIX, Tags
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

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


@router.delete('/{item_id}/')
async def delete(item_id: int,
                 db: Session = Depends(get_db),
                 _: User = Depends(GetCurrentUser())):
    return await Cart.delete(db, item_id)


@router.post('/pay/')
async def pay(db: Session = Depends(get_db),
              current_user: User = Depends(GetCurrentUser())):
    cart_records = db.query(Cart).filter(Cart.buyer_id == current_user.id).all()

    total_cost = sum((record.game.price for record in cart_records))

    current_user_balance = await balance(current_user.id, db, current_user)
    money_amount = json.loads(current_user_balance.body)

    if total_cost > money_amount['balance'] and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds to pay"
        )

    for record in cart_records:
        new_library_record = Library(
            player_id=current_user.id,
            game_id=record.game_id
        )
        await Library.create(db, new_library_record)

        if not current_user.is_superuser:
            game = await Game.by_id(db, record.game_id)
            new_purchase_record = Purchase(
                buyer_id=current_user.id,
                game_id=record.game_id,
                price=game.price
            )
            await Purchase.create(db, new_purchase_record)

        await Cart.delete(db, record.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
