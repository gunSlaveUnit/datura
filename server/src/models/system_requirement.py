from sqlalchemy import Column, String, Text

from server.src.models.entity import Entity


class SystemRequirement(Entity):
    __tablename__ = "system_requirements"

    os = Column(String, nullable=False)
    processor = Column(String, nullable=False)
    memory = Column(String, nullable=False)
    storage = Column(String, nullable=False)
    graphics = Column(String, nullable=False)
    network = Column(String, nullable=False)
    extra = Column(Text, nullable=False)
