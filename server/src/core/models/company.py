from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Session

from server.src.core.models.entity import Entity


class Company(Entity):
    __tablename__ = "companies"

    juridical_name = Column(String, index=True, nullable=False)
    form = Column(String, nullable=False)
    street_house_apartment = Column(String, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    notification_email = Column(String, index=True, nullable=False)
    bic = Column(String, nullable=False)
    bank_address = Column(String, nullable=False)
    bank_account_number = Column(String, nullable=False)
    is_approved = Column(Boolean, nullable=False, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    @staticmethod
    async def by_owner(db: Session, owner_id: int):
        return db.query(Company).filter(Company.owner_id == owner_id).first()
