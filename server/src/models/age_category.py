from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.settings import AgeType


class AgeCategory(Entity):
    __tablename__ = "age_categories"

    title = Column(Enum(AgeType), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)

    games = relationship("Game", back_populates="age_category")
