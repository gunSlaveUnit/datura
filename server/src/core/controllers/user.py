from fastapi import Depends, HTTPException
from starlette import status

from server.src.core.logic.role import RoleLogic
from server.src.core.logic.user import UserLogic
from server.src.core.models.user import User
from server.src.core.settings import RoleType
from server.src.core.utils.crypt import get_password_hash
from server.src.core.utils.db import get_db
from server.src.schemas.auth import SignUpSchema, SignInSchema


class UserController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.user_logic = UserLogic(db)
        self.role_logic = RoleLogic(db)

    async def items(self):
        items = await self.user_logic.items()
        return items.all()

    async def sign_up(self, user_data: SignUpSchema):
        potentially_existing_user_email = await self.user_logic.item_by_email(user_data.email)
        potentially_existing_user_account_name = await self.user_logic.item_by_email(user_data.account_name)

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

        return await self.user_logic.create(user)

    async def sign_in(self, user_data: SignInSchema):
        pass

    async def sign_out(self, session: str):
        pass
