from pydantic import BaseModel


class GameCreateScheme(BaseModel):
    title: str


class GameDBScheme(GameCreateScheme):
    class Config:
        orm_mode = True
