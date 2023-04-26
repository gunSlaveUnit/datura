from pydantic import BaseModel


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
