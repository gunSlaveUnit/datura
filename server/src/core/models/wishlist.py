from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from server.src.core.models.entity import Entity


class Wishlist(Entity):
    __tablename__ = "wishlist"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
    game = relationship("Game", backref="wishlist")
