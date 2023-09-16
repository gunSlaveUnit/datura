from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from server.oldsrc.core.models.entity import Entity


class Library(Entity):
    __tablename__ = "library"

    last_run = Column(Integer)
    game_time = Column(Integer, default=0, nullable=False)

    player_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
    game = relationship("Game", backref="library")
