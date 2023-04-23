from typing import Type, Optional

from sqlalchemy.orm import Session, Query

from server.src.core.models.role import Role
from server.src.core.settings import RoleType


class RoleLogic:
    def __init__(self, db: Session):
        self.db = db

    async def items(self) -> Query:
        return self.db.query(Role)

    async def item_by_title(self, title: RoleType) -> Type[Role]:
        return self.db.query(Role).filter(Role.title == title).one()
