from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity


class GameStatus(Entity):
    __tablename__ = "game_statuses"

    title = Column(String, index=True, nullable=False)
    games = relationship("Game", back_populates="status")
