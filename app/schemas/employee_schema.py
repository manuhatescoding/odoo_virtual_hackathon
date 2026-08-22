from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class EmployeeSchema(BaseModel):
    id: int
    user_id: Optional[int] = None
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    job_title: str
    department: str
    joining_date: date

class EmployeeCreate(BaseModel):
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    job_title: str = "Employee"
    position: Optional[str] = None
    department: str = "General"
    joining_date: Optional[date] = None
    hire_date: Optional[date] = None
    user_id: Optional[int] = None

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    job_title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    hire_date: Optional[date] = None
    joining_date: Optional[date] = None
