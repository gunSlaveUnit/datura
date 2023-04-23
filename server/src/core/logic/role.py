from typing import Type, Any

from sqlalchemy.orm import Session

from server.src.core.logic.logic import Logic
from server.src.core.models.role import Role
from server.src.core.settings import RoleType


class RoleLogic(Logic):
    def __init__(self, db: Session, *args: Any, **kwargs: Any):
        super().__init__(Role, db, *args, **kwargs)

    async def item_by_title(self, title: RoleType) -> Type[Role]:
        return self.db.query(Role).filter(Role.title == title).one()
