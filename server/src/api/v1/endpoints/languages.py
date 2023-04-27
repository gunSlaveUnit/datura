from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.src.api.v1.schemas.language import LanguageCreateSchema
from server.src.core.models.language import Language
from server.src.core.models.user import User
from server.src.core.settings import Tags, LANGUAGES_ROUTER_PREFIX
from server.src.core.utils.auth import get_current_user
from server.src.core.utils.db import get_db

router = APIRouter(prefix=LANGUAGES_ROUTER_PREFIX, tags=[Tags.LANGUAGES])


@router.get('/')
async def items(db: Session = Depends(get_db)):
    return db.query(Language).all()


@router.post('/')
async def create(new_language_data: LanguageCreateSchema,
                 db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    language = Language(**vars(new_language_data))
    return await Language.create(db, language)
