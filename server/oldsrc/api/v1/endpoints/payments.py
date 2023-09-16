from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.payments import PaymentCreateSchema
from server.oldsrc.core.models.payment import Payment
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, PAYMENTS_ROUTER_PREFIX
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=PAYMENTS_ROUTER_PREFIX, tags=[Tags.PAYMENTS])


@router.get('/')
async def items(db: Session = Depends(get_db),
                current_user: User = Depends(GetCurrentUser())):
    return db.query(Payment).filter(Payment.user_id == current_user.id).all()


@router.post('/')
async def create(new_payment: PaymentCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())):
    payment = Payment(user_id=current_user.id, amount=new_payment.amount)
    return await Payment.create(db, payment)
