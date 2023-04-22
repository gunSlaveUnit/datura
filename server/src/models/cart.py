from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.models.game import Game


class Cart(Entity):
    __tablename__ = "cart"

    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)

    game = relationship("Game", backref="cart")
