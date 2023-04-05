from pydantic import BaseModel


class SignInSchema(BaseModel):
    account_name: str
    password: str
