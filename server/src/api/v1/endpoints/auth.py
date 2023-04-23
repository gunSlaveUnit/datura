from fastapi import APIRouter

from server.src.schemas.auth import SignUpSchema
from server.src.core.settings import Tags, AUTH_ROUTER_PREFIX

router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[Tags.AUTH])


@router.post('/sign-up/')
async def sign_up(registration_data: SignUpSchema):
    return user_controller.sign_up()


@router.post('/sign-in/')
async def sign_in():
    pass


@router.post('/sign-out/')
async def sign_out():
    pass
