import decimal

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse, JSONResponse

from server.src.core.models.payment import Payment
from server.src.core.models.purchase import Purchase
from server.src.core.models.user import User
from server.src.core.settings import Tags, AVATARS_PATH, DEFAULT_AVATAR_FILENAME, USERS_ROUTER_PREFIX
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db
from server.src.core.utils.io import remove, save

router = APIRouter(prefix=USERS_ROUTER_PREFIX, tags=[Tags.USERS])


@router.get('/{user_id}/balance/')
async def balance(user_id: int,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(GetCurrentUser())):
    if current_user != user_id or not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: you cannot receive this information"
        )

    payments_total_cost = db.query(func.sum(Payment.amount)).filter(Payment.user_id == user_id).scalar()
    purchases_total_cost = db.query(func.sum(Purchase.price)).filter(Purchase.buyer_id == user_id).scalar()

    current_balance = decimal.Decimal(payments_total_cost) - decimal.Decimal(purchases_total_cost)

    return JSONResponse({
        "balance": current_balance
    })


@router.get('/{user_id}/avatar/')
async def download_avatar(user_id: int,
                          db: Session = Depends(get_db)):
    user = await User.by_id(db, user_id)
    return FileResponse(AVATARS_PATH.joinpath(user.avatar))


@router.put('/{user_id}/avatar/')
async def upload_avatar(user_id: int,
                        file: UploadFile,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(GetCurrentUser())):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot modify this avatar"
        )

    current_avatar_filename = current_user.avatar
    await current_user.update(db, {"avatar": file.filename})

    if current_avatar_filename != DEFAULT_AVATAR_FILENAME:
        await remove(AVATARS_PATH, [current_avatar_filename])

    return await save(AVATARS_PATH, [file])
