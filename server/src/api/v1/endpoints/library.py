from typing import List, Type

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from common.api.v1.schemas.library import LibraryJoinedSchema, LibraryDBSchema, LibraryUpdateSchema
from server.src.core.models.library import Library
from server.src.core.models.user import User
from server.src.core.settings import LIBRARY_ROUTER_PREFIX, Tags
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix=LIBRARY_ROUTER_PREFIX, tags=[Tags.LIBRARY])


@router.get('/', response_model=List[LibraryJoinedSchema | LibraryDBSchema])
async def items(user_id: int | None = None,
                game_id: int | None = None,
                include_games: bool = False,
                db: Session = Depends(get_db),
                _: User = Depends(GetCurrentUser())) -> list[Type[Library]]:
    """
    List of all library records according to the given filters.
    Returns a list of LibraryDBSchema with library record data.
    """

    records_query = db.query(Library)
    if user_id:
        records_query = records_query.filter(Library.player_id == user_id)

    if game_id:
        records_query = records_query.filter(Library.game_id == game_id)

    if include_games:
        records_query = records_query.options(joinedload(Library.game))

    return records_query.all()


@router.put('/{item_id}/', response_model=LibraryDBSchema)
async def update(item_id: int,
                 updated_data: LibraryUpdateSchema,
                 _: User = Depends(GetCurrentUser()),
                 db: Session = Depends(get_db)):
    item = await Library.by_id(db, item_id)
    return await item.update(db, updated_data.dict())
