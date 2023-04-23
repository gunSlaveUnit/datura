from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, Query

from server.src.core.models.user import User


class UserLogic:
    def __init__(self, db: Session):
        self.db = db

    async def items(self) -> Query:
        return self.db.query(User)

    async def item_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    async def item_by_account_name(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.account_name == email).first()

    async def create(self, item: User) -> User:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    async def update(self, item_id: int, new_data: dict) -> User:
        update_user_query = self.db.query(User).filter(User.id == item_id)

        try:
            updatable_user = update_user_query.one()
        except NoResultFound:
            raise ValueError(f"Item with {item_id} id not found")

        update_user_query.update(new_data, synchronize_session=False)
        self.db.commit()
        self.db.refresh(updatable_user)

        return updatable_user
