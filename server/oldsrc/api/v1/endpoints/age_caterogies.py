from fastapi import APIRouter, Depends

from server.oldsrc.core.models.age_category import AgeCategory
from server.oldsrc.core.settings import Tags, AGE_CATEGORIES_ROUTER_PREFIX
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=AGE_CATEGORIES_ROUTER_PREFIX, tags=[Tags.AGE_CATEGORIES])


@router.get('/')
async def items(db=Depends(get_db)):
    return db.query(AgeCategory).all()
