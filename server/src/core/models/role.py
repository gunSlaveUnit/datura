from sqlalchemy import Column, Enum
from sqlalchemy.orm import Session

from server.src.core.models.entity import Entity
from server.src.core.settings import RoleType


class Role(Entity):
    __tablename__ = "roles"

    title = Column(Enum(RoleType), unique=True, index=True, nullable=False)

    @staticmethod
    async def by_title(db: Session,  title: RoleType):
        return db.query(Role).filter(Role.title == title).one()
