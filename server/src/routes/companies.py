from typing import List, Any, Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from server.src.models.company import Company
from server.src.models.user import User
from server.src.schemas.company import CompanyCreateSchema, CompanyDBSchema, ApprovingSchema
from server.src.settings import COMPANIES_ROUTER_PREFIX, Tags
from server.src.utils.auth import get_current_user
from server.src.utils.db import get_db

router = APIRouter(prefix=COMPANIES_ROUTER_PREFIX, tags=[Tags.COMPANIES])


@router.get('/', response_model=List[CompanyDBSchema])
async def every(owner_id: int | None = None,
                db: Session = Depends(get_db)) -> list[Type[Company]]:
    """
    List of all companies according to the given filters.
    Returns a list of CompanyDBScheme with company data.
    """

    companies = db.query(Company)
    if owner_id:
        company = companies.filter(Company.owner_id == owner_id).first()
        if company:
            return [company]
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Company with this owner not found")
    return companies.all()


@router.post('/', response_model=CompanyDBSchema)
async def create(company: CompanyCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)) -> CompanyDBSchema:
    """
    Creating a new company.
    Return a CompanyDBScheme with created entity data.
    """

    potentially_existing_company = db.query(Company).filter(Company.owner_id == current_user.id).first()

    if potentially_existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user already has a registered company"
        )

    company = Company(**vars(company))
    company.owner_id = current_user.id

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


@router.put('/{company_id}/', response_model=CompanyDBSchema)
async def update(company_id: int) -> CompanyDBSchema:
    """
    Updates company fields not related to publish/admin functions.
    Returns a CompanyDBScheme with updated entity data.
    """
    return CompanyDBSchema(title="Updated test company juridical name")


@router.delete('/{company_id}/')
async def delete(company_id: int) -> Response:
    """
    Removes a company with the specified ID.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{company_id}/approve/')
async def approve(company_id: int, approving: ApprovingSchema) -> Response:
    """
    Confirms / denies information about the company.
    If it denies, all games of the company become
    unconfirmed and are not shown in the store.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
