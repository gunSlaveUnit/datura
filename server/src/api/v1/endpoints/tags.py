from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.src.api.v1.schemas.tag import TagCreateSchema
from server.src.core.models.tag import Tag
from server.src.core.models.user import User
from server.src.core.settings import Tags, TAGS_ROUTER_PREFIX
from server.src.core.utils.auth import get_current_user
from server.src.core.utils.db import get_db

router = APIRouter(prefix=TAGS_ROUTER_PREFIX, tags=[Tags.TAGS])


@router.get('/')
async def items(db=Depends(get_db)):
    return db.query(Tag).all()


@router.post('/')
async def create(new_tag_data: TagCreateSchema,
                 db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    tag = Tag(**vars(new_tag_data))
    return await Tag.create(db, tag)
