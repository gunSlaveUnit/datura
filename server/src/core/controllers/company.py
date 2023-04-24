from fastapi import Depends, HTTPException
from starlette import status

from server.src.core.logic.company import CompanyLogic
from server.src.core.logic.game import GameLogic
from server.src.core.logic.game_status import GameStatusLogic
from server.src.core.logic.user import UserLogic
from server.src.core.models.company import Company
from server.src.core.models.game import Game
from server.src.core.models.user import User
from server.src.core.settings import GameStatusType
from server.src.core.utils.db import get_db
from server.src.schemas.company import CompanyCreateSchema, ApprovingSchema


class CompanyController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.user_logic = UserLogic(db)
        self.company_logic = CompanyLogic(db)
        self.game_logic = GameLogic(db)
        self.game_status_logic = GameStatusLogic(db)

    async def items(self):
        items = await self.company_logic.items()
        return items.all()

    async def create(self, company_data: CompanyCreateSchema, current_user: User):
        potentially_existing_company = await self.company_logic.item_by_owner(current_user.id)

        if potentially_existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user already has a registered company"
            )

        company = Company(**vars(company_data))
        company.owner_id = current_user.id

        return await self.company_logic.create(company)

    async def manage_approving(self, company_id: int, approving: ApprovingSchema):
        company_owner = await self.user_logic.item_by_company(company_id)

        not_send_status = await self.game_status_logic.item_by_title(GameStatusType.NOT_SEND)

        if not approving.is_approved:
            self.game_logic.items().filter(Game.owner_id == company_owner).update({"status_id": not_send_status.id})

        await self.company_logic.update(company_id, {"is_approved": approving.is_approved})
