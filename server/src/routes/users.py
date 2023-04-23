from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from server.src.core.models import User
from server.src.schemas import UserDBSchema
from server.src.core.settings import Tags, AVATARS_PATH, DEFAULT_AVATAR_FILENAME
from server.src.core.utils import get_current_user
from server.src.core.utils import get_db
from server.src.core.utils.io import remove, store

router = APIRouter(prefix='/users', tags=[Tags.USERS])


@router.get("/me/", response_model=UserDBSchema)
async def me(current_user: User = Depends(get_current_user)):
    """
    Returns current user data as a UserDBScheme
    """
    return current_user


@router.get('/{user_id}/avatar/')
async def download_avatar(user_id: int,
                          db: Session = Depends(get_db)):
    avatar_filename = db.query(User).filter(User.id == user_id).one().avatar
    return FileResponse(AVATARS_PATH.joinpath(avatar_filename))


@router.put('/{user_id}/avatar/')
async def upload_avatar(user_id: int,
                        file: UploadFile,
                        db: Session = Depends(get_db),
                        _: User = Depends(get_current_user)):
    requested_user_query = db.query(User).filter(User.id == user_id)
    requested_user = requested_user_query.one()
    current_avatar_filename = requested_user.avatar

    requested_user_query.update({"avatar": file.filename}, synchronize_session=False)
    db.commit()

    if current_avatar_filename != DEFAULT_AVATAR_FILENAME:
        await remove(AVATARS_PATH, [current_avatar_filename])

    return await store(AVATARS_PATH, [file])
