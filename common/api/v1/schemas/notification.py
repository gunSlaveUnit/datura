from pydantic import BaseModel


class NotificationCreateSchema(BaseModel):
    user_id: int
    content: str
