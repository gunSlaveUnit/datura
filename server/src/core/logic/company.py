from typing import Any, Optional

from sqlalchemy.orm import Session

from server.src.core.logic.logic import Logic
from server.src.core.models.company import Company


class CompanyLogic(Logic):
    def __init__(self, db: Session, *args: Any, **kwargs: Any):
        super().__init__(Company, db, *args, **kwargs)

    async def item_by_owner(self, owner_id: int) -> Optional[Company]:
        return self.db.query(self.entity).filter(self.entity.owner_id == owner_id).first()
