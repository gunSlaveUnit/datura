from pydantic import BaseModel

from server.src.schemas.entity import EntityDBSchema


class CompanyApprovingSchema(BaseModel):
    is_approved: bool


class CompanyCreateSchema(BaseModel):
    juridical_name: str


class CompanyDBSchema(CompanyCreateSchema, EntityDBSchema):
    class Config:
        orm_mode = True
