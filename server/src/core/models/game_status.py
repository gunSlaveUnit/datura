from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import Session, relationship

from server.src.core.models.entity import Entity
from server.src.core.settings import GameStatusType


class GameStatus(Entity):
    __tablename__ = "game_statuses"

    title = Column(String, unique=True, index=True, nullable=False)
    type = Column(Enum(GameStatusType), unique=True, index=True, nullable=False)

    games = relationship("Game", back_populates="status")

    @staticmethod
    async def by_type(db: Session, title: GameStatusType):
        return db.query(GameStatus).filter(GameStatus.type == title).one()
