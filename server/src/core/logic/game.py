from typing import Any

from sqlalchemy.orm import Session

from server.src.core.logic.logic import Logic
from server.src.core.models.game import Game


class GameLogic(Logic):
    def __init__(self, db: Session, *args: Any, **kwargs: Any):
        super().__init__(Game, db, *args, **kwargs)
