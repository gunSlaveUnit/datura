from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.tag import TagCreateSchema
from server.oldsrc.core.models.tag import Tag
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, TAGS_ROUTER_PREFIX
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=TAGS_ROUTER_PREFIX, tags=[Tags.TAGS])


@router.get('/')
async def items(db=Depends(get_db)):
    return db.query(Tag).all()


@router.post('/')
async def create(new_tag_data: TagCreateSchema,
                 db: Session = Depends(get_db),
                 _: User = Depends(GetCurrentUser())):
    tag = Tag(**vars(new_tag_data))
    return await Tag.create(db, tag)
