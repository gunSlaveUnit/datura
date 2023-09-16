from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.tag import GameTagAssociationCreateSchema
from server.oldsrc.core.models.tag import GameTagAssociation
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, GAME_TAGS_ROUTER_PREFIX
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=GAME_TAGS_ROUTER_PREFIX, tags=[Tags.TAGS])


@router.get('/')
async def items(game_id: int,
                db=Depends(get_db)):
    return db.query(GameTagAssociation).filter(GameTagAssociation.game_id == game_id).all()


@router.post('/')
async def create(game_id: int,
                 new_game_tag_association_data: GameTagAssociationCreateSchema,
                 db: Session = Depends(get_db),
                 _: User = Depends(GetCurrentUser())):
    tag_association = GameTagAssociation(**vars(new_game_tag_association_data))
    tag_association.game_id = game_id

    return await GameTagAssociation.create(db, tag_association)
