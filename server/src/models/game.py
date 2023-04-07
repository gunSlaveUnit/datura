from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.models.game_status import GameStatus
from server.src.models.build import Build
from server.src.models.age import Age
from server.src.models.language import GameLanguage
from server.src.models.review import Review


class Game(Entity):
    # TODO: slight simplification: developer and publisher must be ForeignKeys I think

    __tablename__ = "games"

    title = Column(String, index=True, nullable=False)
    release_date = Column(Integer, index=True)
    developer = Column(String, index=True, nullable=False)
    publisher = Column(String, index=True, nullable=False)
    short_description = Column(Text, nullable=False)
    long_description = Column(Text, nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    directory = Column(String, nullable=False)

    builds = relationship("Build", back_populates="game")

    reviews = relationship("Review", back_populates="game")

    languages = relationship("GameLanguage", back_populates="game")

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    author = relationship("User", back_populates="games")

    status_id = Column(Integer, ForeignKey("game_statuses.id", ondelete="RESTRICT"), index=True, nullable=False)
    status = relationship("GameStatus", back_populates="games")

    age_id = Column(Integer, ForeignKey("ages.id", ondelete="RESTRICT"), index=True, nullable=False)
    age = relationship("Age", back_populates="games")
