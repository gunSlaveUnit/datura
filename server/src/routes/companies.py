from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from schemes.companies import CompanyCreateScheme, CompanyDBScheme, CompanyApprovingScheme
from settings import COMPANIES_ROUTER_PREFIX, Tags

router = APIRouter(prefix=COMPANIES_ROUTER_PREFIX, tags=[Tags.COMPANIES])


@router.get('/', response_model=List[CompanyDBScheme])
async def every() -> List[CompanyDBScheme]:
    """
    List of all companies according to the given filters.
    Returns a list of CompanyDBScheme with company data.
    """

    return [
        CompanyDBScheme(title="Test company juridical name 1"),
        CompanyDBScheme(title="Test company juridical name 2"),
    ]


@router.post('/', response_model=CompanyDBScheme)
async def create(company: CompanyCreateScheme) -> CompanyDBScheme:
    """
    Creating a new company.
    Return a CompanyDBScheme with created entity data.
    """
    return CompanyDBScheme(title="Test company juridical name")


@router.put('/{company_id}/', response_model=CompanyDBScheme)
async def update(company_id: int) -> CompanyDBScheme:
    """
    Updates company fields not related to publish/admin functions.
    Returns a CompanyDBScheme with updated entity data.
    """
    return CompanyDBScheme(title="Updated test company juridical name")


@router.delete('/{company_id}/')
async def delete(company_id: int) -> Response:
    """
    Removes a company with the specified ID.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{company_id}/approve/')
async def approve(company_id: int, approving: CompanyApprovingScheme) -> Response:
    """
    Confirms / denies information about the company.
    If it denies, all games of the company become
    unconfirmed and are not shown in the store.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
