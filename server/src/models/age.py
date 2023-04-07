from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity


class Age(Entity):
    __tablename__ = "ages"

    title = Column(String, unique=True, nullable=False)
    description =  Column(Text, nullable=False)

    games = relationship("Game", back_populates="age")
