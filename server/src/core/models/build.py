from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from server.src.core.models.entity import Entity


class Build(Entity):
    __tablename__ = "builds"

    version = Column(String, nullable=False)
    directory = Column(String, nullable=False)
    call = Column(String, nullable=False)
    params = Column(String)

    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)

    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="RESTRICT"), index=True, nullable=False)
    platform = relationship("Platform", backref="platforms")
