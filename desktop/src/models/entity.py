import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class Entity:
    id: int
    created_at: datetime.datetime
    last_updated_at: datetime.datetime
