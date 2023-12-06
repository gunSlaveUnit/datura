from sqlalchemy import Column, Integer, ForeignKey, Numeric

from server.src.core.models.entity import Entity


class Payment(Entity):
    __tablename__ = "payments"

    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    amount = Column(Numeric(precision=10, scale=2, asdecimal=True))
