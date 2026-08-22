from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class LeaveSchema(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str
    remarks: Optional[str] = None
    admin_comment: Optional[str] = None

class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str = "Pending"
    remarks: Optional[str] = None
    admin_comment: Optional[str] = None
