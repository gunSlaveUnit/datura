from server.src.schemas.auth import SignUpSchema, SignInSchema


class UserController:
    async def sign_up(self, user_data: SignUpSchema):
        pass

    async def sign_in(self, user_data: SignInSchema):
        pass

    async def sign_out(self, session: str):
        pass
