from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Employee, Notification, Payroll, User
from app.schemas import PayrollCreate
from app.utils.dependencies import admin_user, current_user
from app.services.realtime_service import manager

router = APIRouter(prefix="/api/payroll", tags=["payroll"], dependencies=[Depends(current_user)])


@router.get("")
def list_payroll(db: Session = Depends(get_db), user=Depends(current_user)):
    query = db.query(Payroll).order_by(Payroll.effective_date.desc())
    if user.role != "admin":
        query = query.join(Employee).filter(Employee.user_id == user.id)
    records = query.all()
    return [{"id": item.id, "employee_id": item.employee_id, "basic_salary": item.basic_salary, "salary": item.basic_salary, "allowances": item.allowances, "deductions": item.deductions, "net_salary": item.net_salary, "effective_date": item.effective_date, "pay_date": item.effective_date} for item in records]


@router.post("", status_code=201)
async def create_payroll(payload: PayrollCreate, db: Session = Depends(get_db), _admin=Depends(admin_user)):
    if not db.get(Employee, payload.employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    data = payload.model_dump(exclude_none=True)
    basic_salary = data.pop("basic_salary", None) or data.pop("salary", None)
    effective_date = data.pop("effective_date", None) or data.pop("pay_date", None)
    data["basic_salary"] = basic_salary
    data["effective_date"] = effective_date
    data["legacy_salary"] = basic_salary
    data["legacy_pay_date"] = effective_date
    data["net_salary"] = basic_salary + data.get("allowances", 0) - data.get("deductions", 0)
    record = Payroll(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    employee = db.get(Employee, record.employee_id)
    recipients = []
    if employee and employee.user_id:
        recipients.append(employee.user_id)
    recipients.extend(item.id for item in db.query(User).filter(User.role == "admin").all())
    for user_id in set(recipients):
        db.add(Notification(user_id=user_id, title="Payroll updated", message=f"Payroll for {employee.name if employee else 'an employee'} was updated.", category="payroll"))
    db.commit()
    await manager.broadcast("payroll.updated")
    return record
