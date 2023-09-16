import datetime

from fastapi import HTTPException
from sqlalchemy import Column, Integer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from server.oldsrc.core.utils.db import Base


class Entity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(Integer, default=datetime.datetime.now().timestamp(), nullable=False)
    updated_at = Column(Integer, onupdate=datetime.datetime.now().timestamp())

    @classmethod
    async def by_id(cls, db: Session, item_id: int):
        """Returns a concrete object by its ID"""

        item_query = db.query(cls).filter(cls.id == item_id)
        try:
            item = item_query.one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item with this id not found"
            )

        return item

    @staticmethod
    async def create(db: Session, item):
        """Allows to create a new object
        :return created entity
        """

        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    async def update(self, db: Session, new_data: dict):
        """Allows to update information about an object
        :return updated entity
        """

        for attribute, value in new_data.items():
            if hasattr(self, attribute):
                setattr(self, attribute, value)
            else:
                raise AttributeError("The attribute to update does not exist in the source object")

        db.commit()
        db.refresh(self)

        return self

    @classmethod
    async def delete(cls, db: Session, item_id: int):
        """Deletes an object"""

        item = await cls.by_id(db, item_id)

        db.delete(item)
        db.commit()

    def dict(self) -> dict:
        """
        Model attributes excluding SQLAlchemy attributes
        :return: dict without SQLAlchemy attributes
        """
        return {k: v for (k, v) in self.__dict__.items() if '_sa_' != k[:4]}
