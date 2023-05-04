import datetime

from pydantic import BaseModel


class EntityDBSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
