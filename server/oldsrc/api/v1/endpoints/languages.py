from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.language import LanguageCreateSchema
from server.oldsrc.core.models.language import Language
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, LANGUAGES_ROUTER_PREFIX
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=LANGUAGES_ROUTER_PREFIX, tags=[Tags.LANGUAGES])


@router.get('/')
async def items(db: Session = Depends(get_db)):
    return db.query(Language).all()


@router.post('/')
async def create(new_language_data: LanguageCreateSchema,
                 db: Session = Depends(get_db),
                 _: User = Depends(GetCurrentUser())):
    language = Language(**vars(new_language_data))
    return await Language.create(db, language)
