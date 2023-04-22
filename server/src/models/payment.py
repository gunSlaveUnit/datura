from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.models.game import Game
from server.src.models.user import User


class Payment(Entity):
    __tablename__ = "payments"

    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", backref="payments")

    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    game = relationship("Game", backref="payments")

    price = Column(Float, nullable=False)
