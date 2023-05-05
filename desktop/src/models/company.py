from dataclasses import dataclass

from desktop.src.models.entity import Entity


@dataclass
class Company(Entity):
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
    is_approved: bool
    owner_id: int
