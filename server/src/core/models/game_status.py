from sqlalchemy import Column, String

from server.src.core.models.entity import Entity


class GameStatus(Entity):
    __tablename__ = "game_statuses"

    title = Column(String, unique=True, index=True, nullable=False)
