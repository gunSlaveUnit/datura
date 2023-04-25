import datetime

from fastapi import HTTPException
from sqlalchemy import Column, Integer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from server.src.core.utils.db import Base


class Entity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(Integer, default=datetime.datetime.now().timestamp(), nullable=False)
    updated_at = Column(Integer, onupdate=datetime.datetime.now().timestamp())

    @classmethod
    def by_id(cls, db: Session, item_id: int):
        item_query = db.query(cls).filter(cls.id == item_id)
        try:
            item = item_query.one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item with this id not found"
            )

        return item

    def dict(self) -> dict:
        """
        Model attributes excluding SQLAlchemy attributes
        :return: dict without SQLAlchemy attributes
        """
        return {k: v for (k, v) in self.__dict__.items() if '_sa_' != k[:4]}
