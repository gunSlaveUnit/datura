import uuid

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from server.src.models.role import Role
from server.src.schemas.auth import SignInSchema, SignUpSchema
from server.src.models.user import User
from server.src.settings import Tags, SESSION_TTL, RoleType
from server.src.utils.db import get_db, get_session_storage
from server.src.utils.auth import authenticate_user, get_current_user
from server.src.utils.crypt import get_password_hash

router = APIRouter(prefix='/auth', tags=[Tags.AUTH])


@router.post("/sign-up/")
async def sign_up(registration_data: SignUpSchema,
                  db: Session = Depends(get_db),
                  session_storage=Depends(get_session_storage)):
    """
    Registration (creation of a new user).
    Login immediately.
    """
    potentially_existing_user = db.query(User).filter(User.email == registration_data.email).first()

    if potentially_existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"detail": "User with the same email address or account name already exists"}
        )

    user = User(
        email=registration_data.email,
        account_name=registration_data.account_name,
        displayed_name=f'Player #{db.query(User).count() + 1}',
        password=get_password_hash(registration_data.password),
        role_id=db.query(Role).filter(Role.title == RoleType.USER).one().id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return await sign_in(
        SignInSchema(account_name=user.account_name, password=registration_data.password),
        db,
        session_storage
    )


@router.post("/sign-in/")
async def sign_in(login_data: SignInSchema,
                  db: Session = Depends(get_db),
                  session_storage=Depends(get_session_storage)):
    """
    Sets the session id in the request cookie
    if the user is successfully authenticated.
    """
    user: User | None = await authenticate_user(login_data.account_name, login_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"detail": "Incorrect account name or password"}
        )

    session_id = str(uuid.uuid4())
    session_storage.set(session_id, user.id)
    session_storage.expire(session_id, SESSION_TTL)

    response = JSONResponse({"detail": "Logged in successfully"})
    response.set_cookie("session_id", session_id, max_age=SESSION_TTL)
    return response


@router.post("/sign-out/")
async def sign_out(authorization: str = Header(None),
                   _=Depends(get_current_user),
                   session_storage=Depends(get_session_storage)):
    """
    Deletes a user session.
    """
    session_storage.delete(authorization)
    response = JSONResponse({"detail": f"Session {authorization} was removed"})
    return response
