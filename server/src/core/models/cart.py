from sqlalchemy import Column, Integer, ForeignKey

from server.src.core.models.entity import Entity


class Cart(Entity):
    __tablename__ = "cart"

    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
