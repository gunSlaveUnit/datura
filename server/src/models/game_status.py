from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.settings import GameStatusType


class GameStatus(Entity):
    __tablename__ = "game_statuses"

    title = Column(Enum(GameStatusType), unique=True, index=True, nullable=False)
    games = relationship("Game", back_populates="status")
