from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class SignInSchema(BaseModel):
    account_name: str
    password: str


class SignUpSchema(BaseModel):
    email: EmailStr
    account_name: str
    password: str
