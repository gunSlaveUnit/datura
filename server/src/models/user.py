from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity
from server.src.models.game import Game
from server.src.settings import DEFAULT_AVATAR_FILENAME


class User(Entity):
    __tablename__ = "users"

    email = Column(String(255), index=True, nullable=False)
    account_name = Column(String(255), index=True, nullable=False)
    displayed_name = Column(String(255), index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    last_login_at = Column(Integer)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    avatar = Column(String, nullable=False, default=DEFAULT_AVATAR_FILENAME)

    role_id = Column(Integer, ForeignKey('roles.id', ondelete="RESTRICT"), index=True, nullable=False)
    role = relationship("Role", back_populates="users")

    company = relationship("Company", uselist=False, back_populates="master")

    reviews = relationship("Review", back_populates="user")
