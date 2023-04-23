from typing import List, Type

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from server.src.core.models.cart import Cart
from server.src.core.models import Library
from server.src.core.models import User
from server.src.core.schemas.cart import CartDBSchema, CartJoinedSchema, CartCreateSchema
from server.src.settings import CART_ROUTER_PREFIX, Tags
from server.src.core.utils import get_current_user
from server.src.core.utils import get_db

router = APIRouter(prefix=CART_ROUTER_PREFIX, tags=[Tags.CART])


@router.get('/', response_model=List[CartJoinedSchema | CartDBSchema])
async def every(game_id: int | None = None,
        db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> list[Type[Cart]]:
    records_query = db.query(Cart).filter(Cart.buyer_id == current_user.id)

    if game_id:
        records_query = records_query.filter(Cart.game_id == game_id)

    return records_query.all()


@router.post('/', response_model=CartJoinedSchema | CartDBSchema)
async def create(new_record: CartCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)) -> Type[Cart]:
    record = Cart(**vars(new_record))
    record.buyer_id = current_user.id

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.post('/pay/')
async def pay(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    user_cart = await every(db, current_user)

    for record in user_cart:
        new_library_record = Library(
            player_id = current_user.id,
            game_id = record.game_id
        )

        db.add(new_library_record)
        db.delete(record)
        db.commit()

    return JSONResponse({"message": "Payment was successful"})
