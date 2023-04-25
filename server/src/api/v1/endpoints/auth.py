import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Cookie, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from server.src.core.controllers.user import UserController
from server.src.core.models.role import Role
from server.src.core.models.user import User
from server.src.core.utils.auth import get_current_user, authenticate_user
from server.src.core.utils.crypt import get_password_hash
from server.src.core.utils.db import get_session_storage, get_db
from server.src.schemas.auth import SignUpSchema, SignInSchema
from server.src.core.settings import Tags, AUTH_ROUTER_PREFIX, RoleType, SESSION_TTL

router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[Tags.AUTH])


@router.post('/sign-up/')
async def sign_up(registration_data: SignUpSchema,
                  db=Depends(get_db),
                  session_storage=Depends(get_session_storage)):
    """Registration (creation of a new user).
    Login immediately.
    """

    same_email_user = await User.by_email(db, registration_data.email)
    same_account_name_user = await User.by_account_name(db, registration_data.account_name)

    if same_email_user or same_account_name_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same email address or account name already exists"
        )

    default_user_role = await Role.by_title(db, RoleType.USER)

    user = User(
        email=registration_data.email,
        account_name=registration_data.account_name,
        displayed_name=f'Player #{db.query(User).count() + 1}',
        password=get_password_hash(registration_data.password),
        role_id=default_user_role.id
    )

    _ = await User.create(db, user)

    return await sign_in(
        SignInSchema(
            account_name=registration_data.account_name,
            password=registration_data.password
        ),
        db,
        session_storage
    )


@router.post('/sign-in/')
async def sign_in(login_data: SignInSchema,
                  db=Depends(get_db),
                  session_storage=Depends(get_session_storage)):
    user: Optional[User] = await authenticate_user(login_data.account_name, login_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect account name or password"
        )

    session_id = str(uuid.uuid4())
    session_storage.set(session_id, user.id)
    session_storage.expire(session_id, SESSION_TTL)

    response = JSONResponse({"detail": "Logged in successfully"})
    response.set_cookie("session", session_id, max_age=SESSION_TTL)

    await user.update(db, {"login_at": datetime.datetime.now().timestamp()})

    return response


@router.post('/sign-out/')
async def sign_out(session: str = Cookie(),
                   user_controller: UserController = Depends(UserController)):
    return await user_controller.sign_out(session)


@router.get('/me/')
async def me(current_user: User = Depends(get_current_user)):
    return current_user
