from fastapi import APIRouter, Depends, Cookie

from server.src.core.controllers.user import UserController
from server.src.core.models.user import User
from server.src.core.utils.auth import get_current_user
from server.src.schemas.auth import SignUpSchema, SignInSchema
from server.src.core.settings import Tags, AUTH_ROUTER_PREFIX

router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[Tags.AUTH])


@router.post('/sign-up/')
async def sign_up(registration_data: SignUpSchema,
                  user_controller: UserController = Depends(UserController)):
    return await user_controller.sign_up(registration_data)


@router.post('/sign-in/')
async def sign_in(login_data: SignInSchema,
                  user_controller: UserController = Depends(UserController)):
    return await user_controller.sign_in(login_data)


@router.post('/sign-out/')
async def sign_out(session: str = Cookie(),
                   user_controller: UserController = Depends(UserController)):
    return await user_controller.sign_out(session)


@router.get('/me/')
async def me(current_user: User = Depends(get_current_user)):
    return current_user
