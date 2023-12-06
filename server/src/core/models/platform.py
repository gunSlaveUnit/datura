from sqlalchemy import Column, Enum

from server.src.core.models.entity import Entity
from server.src.core.settings import PlatformType


class Platform(Entity):
    __tablename__ = "platforms"

    title = Column(Enum(PlatformType), unique=True, index=True, nullable=False)
