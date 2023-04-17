from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.models.game_status import GameStatus
from server.src.models.build import Build
from server.src.models.age_category import AgeCategory
from server.src.models.language import GameLanguage
from server.src.models.review import Review
from server.src.models.company import Company


class Game(Entity):
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

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False)
    company = relationship("Company", back_populates="games")

    status_id = Column(Integer, ForeignKey("game_statuses.id", ondelete="RESTRICT"), index=True, nullable=False)
    status = relationship("GameStatus", back_populates="games")

    age_category_id = Column(Integer, ForeignKey("age_categories.id", ondelete="RESTRICT"), index=True, nullable=False)
    age_category = relationship("AgeCategory", back_populates="games")
