from datetime import date as DateType, datetime
from typing import Optional
from pydantic import BaseModel, Field

class AttendanceSchema(BaseModel):
    id: int
    employee_id: int
    check_in: datetime
    check_out: Optional[datetime] = None
    date: DateType
    status: str

class AttendanceCreate(BaseModel):
    employee_id: int
    check_in: datetime
    check_out: Optional[datetime] = None
    date: DateType = Field(default_factory=DateType.today)
    status: str = "Present"
