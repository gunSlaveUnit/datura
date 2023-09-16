from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Session

from server.oldsrc.core.models.entity import Entity
from server.oldsrc.core.settings import DEFAULT_AVATAR_FILENAME


class User(Entity):
    __tablename__ = "users"

    email = Column(String(255), index=True, nullable=False)
    account_name = Column(String(255), index=True, nullable=False)
    displayed_name = Column(String(255), index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    login_at = Column(Integer)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    avatar = Column(String, nullable=False, default=DEFAULT_AVATAR_FILENAME)

    role_id = Column(Integer, ForeignKey('roles.id', ondelete="RESTRICT"), index=True, nullable=False)

    @staticmethod
    async def by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def by_account_name(db: Session, account_name: str):
        return db.query(User).filter(User.account_name == account_name).first()
