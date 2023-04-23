import datetime
import uuid
from typing import Optional

from fastapi import Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from server.src.core.logic.role import RoleLogic
from server.src.core.logic.user import UserLogic
from server.src.core.models.user import User
from server.src.core.settings import RoleType, SESSION_TTL
from server.src.core.utils.auth import authenticate_user
from server.src.core.utils.crypt import get_password_hash
from server.src.core.utils.db import get_db, get_session_storage
from server.src.schemas.auth import SignUpSchema, SignInSchema


class UserController:
    def __init__(self, db=Depends(get_db), session_storage=Depends(get_session_storage)):
        self.db = db
        self.session_storage = session_storage
        self.user_logic = UserLogic(db)
        self.role_logic = RoleLogic(db)

    async def items(self):
        items = await self.user_logic.items()
        return items.all()

    async def sign_up(self, user_data: SignUpSchema):
        """Registration (creation of a new user).
        Login immediately.
        """

        potentially_existing_user_email: Optional[User] = await self.user_logic.item_by_email(user_data.email)
        potentially_existing_user_account_name: Optional[User] = await self.user_logic.item_by_email(user_data.account_name)

        if potentially_existing_user_email or potentially_existing_user_account_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"detail": "User with the same email address or account name already exists"}
            )

        default_user_role = await self.role_logic.item_by_title(RoleType.USER)
        user = User(
            email=user_data.email,
            account_name=user_data.account_name,
            displayed_name=f'Player #{self.db.query(User).count() + 1}',
            password=get_password_hash(user_data.password),
            role_id=default_user_role.id
        )

        _ = await self.user_logic.create(user)

        return await self.sign_in(
            SignInSchema(
                account_name=user_data.account_name,
                password=user_data.password
            )
        )

    async def sign_in(self, user_data: SignInSchema):
        """Sets the session id in the request cookie
        if the user is successfully authenticated.
        """

        user: Optional[User] = await authenticate_user(user_data.account_name, user_data.password, self.db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"detail": "Incorrect account name or password"}
            )

        session_id = str(uuid.uuid4())
        self.session_storage.set(session_id, user.id)
        self.session_storage.expire(session_id, SESSION_TTL)

        response = JSONResponse({"detail": "Logged in successfully"})
        response.set_cookie("session", session_id, max_age=SESSION_TTL)

        await self.user_logic.update(user.id, {"login_at": datetime.datetime.now().timestamp()})

        return response

    async def sign_out(self, session: str):
        pass
