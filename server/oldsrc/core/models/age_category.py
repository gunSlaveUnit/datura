from sqlalchemy import Column, Text, Enum

from server.oldsrc.core.models.entity import Entity
from server.oldsrc.core.settings import AgeType


class AgeCategory(Entity):
    __tablename__ = "age_categories"

    title = Column(Enum(AgeType), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
