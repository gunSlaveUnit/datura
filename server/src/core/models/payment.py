from sqlalchemy import Column, Integer, ForeignKey, Float

from server.src.core.models.entity import Entity


class Payment(Entity):
    __tablename__ = "payments"

    price = Column(Float, nullable=False)

    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)

    game_id = Column(Integer, ForeignKey("games.id"), index=True)
