from sqlalchemy import Column, Enum

from server.src.core.models.entity import Entity
from server.src.settings import GameStatusType


class GameStatus(Entity):
    __tablename__ = "game_statuses"

    title = Column(Enum(GameStatusType), unique=True, index=True, nullable=False)
