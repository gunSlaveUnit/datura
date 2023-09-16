from fastapi import APIRouter, Depends

from server.oldsrc.core.models.platform import Platform
from server.oldsrc.core.settings import Tags, PLATFORMS_ROUTER_PREFIX
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=PLATFORMS_ROUTER_PREFIX, tags=[Tags.PLATFORMS])


@router.get('/')
async def items(db=Depends(get_db)):
    return db.query(Platform).all()
