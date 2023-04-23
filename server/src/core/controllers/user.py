from fastapi import Depends

from server.src.core.logic.user import UserLogic
from server.src.core.utils.db import get_db
from server.src.schemas.auth import SignUpSchema, SignInSchema


class UserController:
    def __init__(self, db = Depends(get_db)):
        self.user_logic = UserLogic(db)

    async def items(self):
        items = await self.user_logic.items()
        return items.all()

    async def sign_up(self, user_data: SignUpSchema):
        pass

    async def sign_in(self, user_data: SignInSchema):
        pass

    async def sign_out(self, session: str):
        pass
