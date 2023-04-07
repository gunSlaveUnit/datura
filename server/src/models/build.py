from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.models.platform import Platform
from server.src.models.system_requirement import SystemRequirement


class Build(Entity):
    __tablename__ = "builds"

    directory = Column(String, nullable=False)
    call = Column(String, nullable=False)
    params = Column(String, nullable=False)

    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
    game = relationship("Game", back_populates="builds")

    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="RESTRICT"), index=True, nullable=False)
    platform = relationship("Platform", backref="platforms")

    requirements_id = Column(Integer, ForeignKey("system_requirements.id", ondelete="RESTRICT"), index=True, nullable=False)
    requirements = relationship("SystemRequirement",backref="system_requirements")
