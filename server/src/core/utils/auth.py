from typing import Tuple

from fastapi import HTTPException, Depends, Cookie
from sqlalchemy.orm import Session
from starlette import status

from server.src.core.models.role import Role
from server.src.core.models.user import User
from server.src.core.settings import RoleType
from server.src.core.utils.crypt import crypt_context
from server.src.core.utils.db import get_db, get_session_storage


async def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


async def authenticate_user(account_name: str, password: str, db):
    user = db.query(User).filter(User.account_name == account_name).first()
    if user and await verify_password(password, user.password):
        return user
    return None


async def _get_current_user(scopes: Tuple[RoleType],
                            is_required=True,
                            session: str = Cookie(None),
                            db: Session = Depends(get_db),
                            session_storage=Depends(get_session_storage)):
    if session is None:
        if is_required:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session ID not provided"
            )
        else:
            return None

    user_id = session_storage.get(session)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has expired. Please re-login"
        )

    user = await User.by_id(db, int(user_id))

    possible_roles = []
    for scope in scopes:
        role = await Role.by_title(db, scope)
        possible_roles.append(role.id)

    if user.role_id not in possible_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: you do not have sufficient rights to perform this operation"
        )

    return user


class GetCurrentUser:
    def __init__(self, scopes: Tuple[RoleType] = None, is_required: bool = True):
        self.scopes = scopes
        self.is_required = is_required

    async def __call__(self,
                       session: str = Cookie(None),
                       db: Session = Depends(get_db),
                       session_storage=Depends(get_session_storage)):
        if self.scopes is None:
            self.scopes = RoleType.USER, RoleType.ADMIN

        return await _get_current_user(self.scopes, self.is_required, session, db, session_storage)
