from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity


class Library(Entity):
    __tablename__ = "library"

    player_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    user = relationship("User", backref="library")

    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
    game = relationship("Game", backref="library")

    last_run = Column(Integer)
    game_time = Column(Integer, default=0, nullable=False)
