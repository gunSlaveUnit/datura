from pydantic import BaseModel


class NotificationCreateSchema(BaseModel):
    user_id: int
    body: str
