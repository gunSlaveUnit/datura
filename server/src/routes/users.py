from fastapi import APIRouter, Depends

from server.src.models.user import User
from server.src.schemas.user import UserDBSchema
from server.src.settings import Tags
from server.src.utils.auth import get_current_user

router = APIRouter(prefix='/users', tags=[Tags.USERS])


@router.get("/me/", response_model=UserDBSchema)
async def me(current_user: User = Depends(get_current_user)):
    """
    Returns current user data as a UserDBScheme
    """
    return current_user
