import datetime

from sqlalchemy import Column, Integer

from server.src.utils.db import Base


class Entity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(Integer, default=datetime.datetime.now().timestamp(), nullable=False)
    last_updated_at = Column(Integer, onupdate=datetime.datetime.now().timestamp())

    def dict(self) -> dict:
        """
        Model attributes excluding SQLAlchemy attributes
        :return: dict without SQLAlchemy attributes
        """
        return {k: v for (k, v) in self.__dict__.items() if '_sa_' != k[:4]}
