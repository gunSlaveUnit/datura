from typing import Optional, Any

from sqlalchemy.orm import Session

from server.src.core.logic.logic import Logic
from server.src.core.models.user import User


class UserLogic(Logic):
    def __init__(self, db: Session, *args: Any, **kwargs: Any):
        super().__init__(User, db, *args, **kwargs)

    async def item_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    async def item_by_account_name(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.account_name == email).first()

    async def item_by_company(self, company_id: int) -> Optional[User]:
        return self.db.query(User).filter(self.entity.id == company_id).first()
