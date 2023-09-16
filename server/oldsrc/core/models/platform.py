from sqlalchemy import Column, Enum

from server.oldsrc.core.models.entity import Entity
from server.oldsrc.core.settings import PlatformType


class Platform(Entity):
    __tablename__ = "platforms"

    title = Column(Enum(PlatformType), unique=True, index=True, nullable=False)
