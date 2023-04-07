from sqlalchemy import Column, String

from server.src.models.entity import Entity


class Platform(Entity):
    __tablename__ = "platforms"

    title = Column(String, index=True, nullable=False)
