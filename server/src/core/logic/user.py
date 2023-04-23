from sqlalchemy.orm import Session, Query

from server.src.core.models.user import User


class UserLogic:
    def __init__(self, db: Session):
        self.db = db

    async def items(self) -> Query:
        return self.db.query(User)
