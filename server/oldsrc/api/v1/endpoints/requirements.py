from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.requirements import RequirementsCreateSchema
from server.oldsrc.core.models.system_requirement import SystemRequirement
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, SYSTEM_REQUIREMENTS_ROUTER_PREFIX
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=SYSTEM_REQUIREMENTS_ROUTER_PREFIX, tags=[Tags.SYSTEM_REQUIREMENTS])


@router.get('/')
async def items(game_id: int,
                build_id: int,
                db: Session = Depends(get_db)):
    return db.query(SystemRequirement).filter(SystemRequirement.build_id == build_id).all()


@router.post('/')
async def create(game_id: int,
                 build_id: int,
                 new_requirements_data: RequirementsCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())):
    requirements = SystemRequirement(**vars(new_requirements_data))
    requirements.build_id = build_id
    return await SystemRequirement.create(db, requirements)
