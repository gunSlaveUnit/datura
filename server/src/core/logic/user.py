from typing import Optional

from sqlalchemy.orm import Session, Query

from server.src.core.models.user import User


class UserLogic:
    def __init__(self, db: Session):
        self.db = db

    async def items(self) -> Query:
        return self.db.query(User)

    async def create(self, item: User) -> User:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
