from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse

from server.src.core.models.user import User
from server.src.core.settings import Tags, AVATARS_PATH, DEFAULT_AVATAR_FILENAME, USERS_ROUTER_PREFIX
from server.src.core.utils.auth import get_current_user
from server.src.core.utils.db import get_db
from server.src.core.utils.io import remove, save

router = APIRouter(prefix=USERS_ROUTER_PREFIX, tags=[Tags.USERS])


@router.get('/{user_id}/avatar/')
async def download_avatar(user_id: int,
                          db: Session = Depends(get_db)):
    user = await User.by_id(db, user_id)
    return FileResponse(AVATARS_PATH.joinpath(user.avatar))


@router.put('/{user_id}/avatar/')
async def upload_avatar(user_id: int,
                        file: UploadFile,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot modify this avatar"
        )

    current_avatar_filename = current_user.avatar
    await current_user.update(db, {"avatar": file.filename})

    if current_avatar_filename != DEFAULT_AVATAR_FILENAME:
        await remove(AVATARS_PATH, [current_avatar_filename])

    return await save(AVATARS_PATH, [file])
