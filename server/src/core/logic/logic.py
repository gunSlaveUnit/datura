from abc import ABC
from typing import Any

from fastapi import Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from server.src.core.models.entity import Entity


class Logic(ABC):
    """Abstract class to provide a base CRUD functionality for any Entity classes"""

    entity: Entity = NotImplementedError
    db: Session = NotImplementedError

    def __init__(self, entity: Entity, db: Session, *args: Any, **kwargs: Any):
        """Create a logic
        :param entity - any instance of Entity class
        :param db - SQLAlchemy database session
        """

        super().__init__(*args, **kwargs)

        self.entity = entity
        self.db = db

    async def items(self) -> Query:
        """Returns the base query for further filters, selections, groupings"""

        return self.db.query(self.entity)

    async def item_by_id(self, item_id: int):
        """Returns a concrete object by its ID"""

        item_query = self.db.query(self.entity).filter(self.entity.id == item_id)

        try:
            item = item_query.one()
        except NoResultFound:
            raise ValueError(f"Item with {item_id} id not found")

        return item

    async def create(self, entity: Entity) -> Entity:
        """Allows to create a new object
        :return created entity
        """

        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    async def update(self, item_id: int, new_data: dict) -> Entity:
        """Allows to update information about an object
        :return updated entity
        """

        update_user_query = self.db.query(self.entity).filter(self.entity.id == item_id)

        try:
            updatable_user = update_user_query.one()
        except NoResultFound:
            raise ValueError(f"Item with {item_id} id not found")

        update_user_query.update(new_data, synchronize_session=False)
        self.db.commit()
        self.db.refresh(updatable_user)

        return updatable_user

    def delete(self, item_id: int) -> None:
        """Deletes an object"""

        item = self.item_by_id(item_id)
        self.db.delete(item)
        self.db.commit()
