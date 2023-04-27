from fastapi import APIRouter, Depends

from server.src.core.models.platform import Platform
from server.src.core.settings import Tags, PLATFORMS_ROUTER_PREFIX
from server.src.core.utils.db import get_db

router = APIRouter(prefix=PLATFORMS_ROUTER_PREFIX, tags=[Tags.PLATFORMS])


@router.get('/')
async def items(db=Depends(get_db)):
    return db.query(Platform).all()
