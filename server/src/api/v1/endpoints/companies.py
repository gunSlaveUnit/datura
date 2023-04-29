from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from server.src.core.models.company import Company
from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.models.user import User
from server.src.core.settings import Tags, COMPANIES_ROUTER_PREFIX, GameStatusType
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db
from server.src.api.v1.schemas.company import CompanyCreateSchema, ApprovingSchema

router = APIRouter(prefix=COMPANIES_ROUTER_PREFIX, tags=[Tags.COMPANIES])


@router.get('/')
async def items(owner_id: int = Query(None),
                db=Depends(get_db),
                current_user: User = Depends(GetCurrentUser())):
    """List of all companies according to the given filters."""

    if owner_id and owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: you cannot receive this information"
        )

    companies = db.query(Company)
    if owner_id:
        company = companies.filter(Company.owner_id == owner_id).first()
        if company:
            return [company]
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Company with this owner not found")

    return companies.all()


@router.post('/')
async def create(new_company_data: CompanyCreateSchema,
                 current_user: User = Depends(GetCurrentUser()),
                 db=Depends(get_db)):
    potentially_existing_company = await Company.by_owner(db, current_user.id)

    if potentially_existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user already has a registered company"
        )

    company = Company(**vars(new_company_data))
    company.owner_id = current_user.id

    return await Company.create(db, company)


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

    not_approved_status = await GameStatus.by_title(db, GameStatusType.NOT_APPROVED)

    company_games = db.query(Game).filter(Game.owner_id == company_owner_id)
    if not approving.is_approved:
        company_games.update({"status_id": not_approved_status.id})

    await company.update(db, {"is_approved": approving.is_approved})
