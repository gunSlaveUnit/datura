from pydantic import BaseModel


class GameApprovingScheme(BaseModel):
    is_approved: bool


class GameCreateScheme(BaseModel):
    title: str


class GameDBScheme(GameCreateScheme):
    class Config:
        orm_mode = True
