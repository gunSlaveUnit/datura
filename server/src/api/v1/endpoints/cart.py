from typing import List, Type

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from server.src.api.v1.schemas.cart import CartJoinedSchema, CartDBSchema, CartCreateSchema
from server.src.core.models.cart import Cart
from server.src.core.models.library import Library
from server.src.core.models.user import User
from server.src.core.settings import CART_ROUTER_PREFIX, Tags
from server.src.core.utils.auth import _get_current_user, GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix=CART_ROUTER_PREFIX, tags=[Tags.CART])


@router.get('/', response_model=List[CartJoinedSchema | CartDBSchema])
async def items(db: Session = Depends(get_db),
                current_user: User = Depends(GetCurrentUser)) -> list[Type[Cart]]:
    return db.query(Cart).filter(Cart.buyer_id == current_user.id).all()


@router.post('/', response_model=CartDBSchema)
async def create(new_record: CartCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser)) -> Type[Cart]:
    record = Cart(**vars(new_record))
    record.buyer_id = current_user.id

    return await Cart.create(db, record)


@router.post('/pay/')
async def pay(db: Session = Depends(get_db),
              current_user: User = Depends(GetCurrentUser)):
    user_cart = await items(db, current_user)

    for record in user_cart:
        new_library_record = Library(
            player_id=current_user.id,
            game_id=record.game_id
        )

        await Cart.create(db, new_library_record)
        await Cart.delete(db, record.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
