from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from server.src.core.controllers.company import CompanyController
from server.src.core.models.company import Company
from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.models.user import User
from server.src.core.settings import Tags, COMPANIES_ROUTER_PREFIX, GameStatusType
from server.src.core.utils.auth import get_current_user
from server.src.core.utils.db import get_db
from server.src.schemas.company import CompanyCreateSchema, ApprovingSchema

router = APIRouter(prefix=COMPANIES_ROUTER_PREFIX, tags=[Tags.COMPANIES])


@router.get('/')
async def items(company_controller: CompanyController = Depends(CompanyController)):
    return await company_controller.items()


@router.post('/')
async def create(new_company_data: CompanyCreateSchema,
                 current_user: User = Depends(get_current_user),
                 company_controller: CompanyController = Depends(CompanyController)):
    return await company_controller.create(new_company_data, current_user)


@router.patch('/{company_id}/approve/')
async def approve(company_id: int,
                  approving: ApprovingSchema,
                  db=Depends(get_db)):
    """Confirms / denies information about the company.
    If it denies, all games of the company become
    unconfirmed and are not shown in the store.
    """

    company = await Company.by_id(db, company_id)

    company_owner_id = company.owner_id

    not_send_status = await GameStatus.by_title(db, GameStatusType.NOT_SEND)

    company_games = db.query(Game).filter(Game.owner_id == company_owner_id)
    if not approving.is_approved:
        company_games.update({"status_id": not_send_status.id})

    await company.update({"is_approved": approving.is_approved})
