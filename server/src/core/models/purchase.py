from sqlalchemy import Column, Integer, ForeignKey, Float

from server.src.core.models.entity import Entity


class Purchase(Entity):
    __tablename__ = "purchases"

    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    price = Column(Float, nullable=False)
