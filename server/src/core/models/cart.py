from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from server.src.core.models.entity import Entity


class Cart(Entity):
    __tablename__ = "cart"

    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)

    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    game = relationship("Game", backref="cart")
