from fastapi import APIRouter

from server.src.settings import Tags

router = APIRouter(prefix='/auth', tags=[Tags.AUTH])


@router.post("/sign-up/")
async def sign_up():
    """
    Registration (creation of a new user).
    Login immediately.
    """
    pass


@router.post("/sign-in/")
async def sign_in():
    """
    Sets the session id in the request cookie
    if the user is successfully authenticated.
    """
    pass
