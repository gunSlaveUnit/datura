from fastapi import HTTPException, Depends, Cookie
from sqlalchemy.orm import Session
from starlette import status

from server.src.core.models.user import User
from server.src.core.utils.crypt import crypt_context
from server.src.core.utils.db import get_db, get_session_storage


async def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


async def authenticate_user(account_name: str, password: str, db):
    user = db.query(User).filter(User.account_name == account_name).first()
    if user and await verify_password(password, user.password):
        return user
    return None


async def get_current_user(session: str = Cookie(None),
                           db: Session = Depends(get_db),
                           session_storage=Depends(get_session_storage)):
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID not provided"
        )

    user_id = session_storage.get(session)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has expired. Please re-login"
        )

    return db.query(User).filter(User.id == int(user_id)).one()
