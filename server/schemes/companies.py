from pydantic import BaseModel


class CompanyCreateScheme(BaseModel):
    juridical_name: str


class CompanyDBScheme(CompanyCreateScheme):
    class Config:
        orm_mode = True
