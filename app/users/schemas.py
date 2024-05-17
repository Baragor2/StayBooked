from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    hashed_password: str
