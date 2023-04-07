from sqlalchemy import Column, Enum, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.settings import RoleType


class Build(Entity):
    __tablename__ = "builds"

    title = Column(String, unique=True, nullable=False)
    call = Column(String, nullable=False)
    params = Column(String, nullable=False)
    directory = Column(String, nullable=False)

    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
    game = relationship("Game", back_populates="builds")

    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="RESTRICT"), index=True, nullable=False)
    platform = relationship("Platform", backref="platforms")
