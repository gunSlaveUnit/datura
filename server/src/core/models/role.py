from sqlalchemy import Column, Enum

from server.src.core.models.entity import Entity
from server.src.settings import RoleType


class Role(Entity):
    __tablename__ = "roles"

    title = Column(Enum(RoleType), unique=True, index=True, nullable=False)
