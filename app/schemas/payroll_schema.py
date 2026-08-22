from datetime import date
from pydantic import BaseModel, Field

class PayrollSchema(BaseModel):
    id: int
    employee_id: int
    basic_salary: float
    allowances: float
    deductions: float
    net_salary: float
    effective_date: date

class PayrollCreate(BaseModel):
    employee_id: int
    basic_salary: float | None = Field(default=None, gt=0)
    allowances: float = Field(default=0.0, ge=0)
    salary: float | None = Field(default=None, gt=0)
    effective_date: date | None = None
    pay_date: date | None = None
    deductions: float = Field(default=0.0, ge=0)
