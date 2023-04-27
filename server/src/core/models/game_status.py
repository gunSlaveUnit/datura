from sqlalchemy import Column, Enum
from sqlalchemy.orm import Session

from server.src.core.models.entity import Entity
from server.src.core.settings import GameStatusType


class GameStatus(Entity):
    __tablename__ = "game_statuses"

    title = Column(Enum(GameStatusType), unique=True, index=True, nullable=False)

    @staticmethod
    async def by_title(db: Session, title: GameStatusType):
        return db.query(GameStatus).filter(GameStatus.title == title).one()
