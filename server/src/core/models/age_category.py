from sqlalchemy import Column, Text, Enum

from server.src.core.models.entity import Entity
from server.src.core.settings import AgeType


class AgeCategory(Entity):
    __tablename__ = "age_categories"

    title = Column(Enum(AgeType), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
