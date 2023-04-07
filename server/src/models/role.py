from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.settings import RoleType


class Role(Entity):
    __tablename__ = "roles"

    title = Column(Enum(RoleType), unique=True, index=True, nullable=False)

    users = relationship("User", back_populates="role")
