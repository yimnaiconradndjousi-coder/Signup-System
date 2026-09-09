from pydantic import BaseModel, EmailStr, Field, ValidationError

class SignupData(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)