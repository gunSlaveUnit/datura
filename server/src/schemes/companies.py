from pydantic import BaseModel

from server.src.schemes.entity import EntityDBScheme


class CompanyApprovingScheme(BaseModel):
    is_approved: bool


class CompanyCreateScheme(BaseModel):
    juridical_name: str


class CompanyDBScheme(CompanyCreateScheme, EntityDBScheme):
    class Config:
        orm_mode = True
