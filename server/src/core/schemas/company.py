from pydantic import BaseModel

from server.src.core.schemas.entity import EntityDBSchema


class ApprovingSchema(BaseModel):
    is_approved: bool = False


class CompanyCreateSchema(BaseModel):
    juridical_name: str
    form: str
    street_house_apartment: str
    city: str
    region: str
    country: str
    postal_code: str
    notification_email: str
    bic: str
    bank_address: str
    bank_account_number: str


class CompanyDBSchema(CompanyCreateSchema, EntityDBSchema):
    is_approved: bool
    owner_id: int

    class Config:
        orm_mode = True
