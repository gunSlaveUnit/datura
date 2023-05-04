from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.src.api.v1.schemas.payments import PaymentDBSchema, PaymentCreateSchema
from server.src.core.models.payment import Payment
from server.src.core.models.user import User
from server.src.core.settings import Tags, PAYMENTS_ROUTER_PREFIX
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix=PAYMENTS_ROUTER_PREFIX, tags=[Tags.PAYMENTS])


@router.get('/')
async def items(db: Session = Depends(get_db),
                current_user: User = Depends(GetCurrentUser())):
    return db.query(Payment).filter(Payment.user_id == current_user.id).all()


@router.post('/', response_model=PaymentDBSchema)
async def create(new_payment: PaymentCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())):
    payment = Payment(user_id=current_user.id, amount=new_payment.amount)
    return await Payment.create(db, payment)
