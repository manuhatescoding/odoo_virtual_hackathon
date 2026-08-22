from typing import Literal
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    employee_id: int | None = None
    email_verified: bool = False

class UserCreate(BaseModel):
    employee_id: str | None = None
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=1, max_length=120)
    role: str = "employee"

class UserLogin(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str
    login_as: Literal["employee", "admin"] = "employee"
