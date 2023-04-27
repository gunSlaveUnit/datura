from fastapi import APIRouter, Depends

from server.src.core.models.age_category import AgeCategory
from server.src.core.settings import Tags, AGE_CATEGORIES_ROUTER_PREFIX
from server.src.core.utils.db import get_db

router = APIRouter(prefix=AGE_CATEGORIES_ROUTER_PREFIX, tags=[Tags.AGE_CATEGORIES])


@router.get('/')
async def items(db=Depends(get_db)):
    return db.query(AgeCategory).all()
