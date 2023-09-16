from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from common.api.v1.schemas.company import CompanyCreateSchema, ApprovingSchema
from common.api.v1.schemas.notification import NotificationCreateSchema
from server.oldsrc.api.v1.endpoints import notifications
from server.oldsrc.core.models.company import Company
from server.oldsrc.core.models.game import Game
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, COMPANIES_ROUTER_PREFIX, RoleType
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=COMPANIES_ROUTER_PREFIX, tags=[Tags.COMPANIES])


@router.get('/')
async def items(owner_id: int | None = Query(None),
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


@router.get('/{company_id}/')
async def item(company_id: int,
               db=Depends(get_db)):
    return await Company.by_id(db, company_id)


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
                  db=Depends(get_db),
                  current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,)))):
    """Confirms / denies information about the company.
    If it denies, all games of the company become
    unconfirmed and are not shown in the store.
    """

    company = await Company.by_id(db, company_id)

    company_owner_id = company.owner_id

    company_games = db.query(Game).filter(Game.owner_id == company_owner_id)
    if not approving.is_approved:
        company_games.update({
            "is_approved": False,
            "is_send_for_verification": False,
            "is_published": False
        })

    if approving.is_approved:
        owner = await User.by_id(db, company_owner_id)
        email_notification_body = f"Уважаемый {owner.account_name}! " \
                                  "Сведения о Вашей компании были успешно проверены и одобрены. " \
                                  "Вы можете публиковать новые релизы. Надеемся на долгое и плодотворное сотрудничество. " \
                                  "Спасибо, что пользуетесь нашими услугами! С уважением, команда Foggie."
        notification = NotificationCreateSchema(user_id=company_owner_id, content=email_notification_body)
        await notifications.create(notification, db, current_user)

    await company.update(db, {"is_approved": approving.is_approved})
