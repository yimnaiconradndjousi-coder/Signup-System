from pydantic import BaseModel, EmailStr, Field

class SignupData(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)

class LoginData(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)