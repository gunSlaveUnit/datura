from typing import Any

from sqlalchemy.orm import Session

from server.src.core.logic.logic import Logic
from server.src.core.models.game import Game
from server.src.core.models.game_status import GameStatus
from server.src.core.settings import GameStatusType


class GameStatusLogic(Logic):
    def __init__(self, db: Session, *args: Any, **kwargs: Any):
        super().__init__(GameStatus, db, *args, **kwargs)

    async def item_by_title(self, title: GameStatusType):
        return self.db.query(GameStatus).filter(GameStatus.title == title).one()
