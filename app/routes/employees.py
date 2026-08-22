from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate
from app.utils.dependencies import admin_user, current_user
from app.services.realtime_service import manager

router = APIRouter(prefix="/api/employees", tags=["employees"], dependencies=[Depends(current_user)])


def employee_response(employee):
    return {"id": employee.id, "user_id": employee.user_id, "name": employee.name, "first_name": employee.first_name, "last_name": employee.last_name, "phone": employee.phone, "address": employee.address, "profile_picture": employee.profile_picture, "job_title": employee.job_title, "position": employee.job_title, "department": employee.department, "joining_date": employee.joining_date, "hire_date": employee.joining_date}


@router.get("")
def list_employees(db: Session = Depends(get_db), user=Depends(current_user)):
    query = db.query(Employee).order_by(Employee.id)
    if user.role != "admin":
        query = query.filter(Employee.user_id == user.id)
    return [employee_response(employee) for employee in query.all()]


@router.get("/me/profile")
def get_my_profile(db: Session = Depends(get_db), user=Depends(current_user)):
    employee = db.query(Employee).filter(Employee.user_id == user.id).first()
    if employee:
        return employee_response(employee)
    return {"id": None, "user_id": user.id, "name": user.full_name, "phone": None, "address": None, "profile_picture": None, "job_title": "HR Administrator", "position": "HR Administrator", "department": "People Operations", "joining_date": None, "hire_date": None}


@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_response(employee)


@router.patch("/me/profile")
def update_my_profile(payload: EmployeeUpdate, db: Session = Depends(get_db), user=Depends(current_user)):
    employee = db.query(Employee).filter(Employee.user_id == user.id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee profile not found")
    data = payload.model_dump(exclude_unset=True, exclude_none=True)
    permitted = {"phone", "address", "profile_picture"}
    for key in permitted.intersection(data):
        setattr(employee, key, data[key])
    db.commit()
    db.refresh(employee)
    return employee_response(employee)


@router.post("", status_code=201)
async def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db), _admin=Depends(admin_user)):
    data = payload.model_dump(exclude_none=True)
    name = data.pop("name", None) or " ".join(part for part in [data.pop("first_name", ""), data.pop("last_name", "")] if part).strip() or "Unnamed employee"
    joining_date = data.pop("joining_date", None) or data.pop("hire_date", None)
    data.pop("position", None)
    names = name.split(" ", 1)
    employee = Employee(name=name, legacy_first_name=names[0], legacy_last_name=names[1] if len(names) > 1 else "", joining_date=joining_date, **data)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    await manager.broadcast("employees.updated")
    return employee_response(employee)


@router.put("/{employee_id}")
async def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db), _admin=Depends(admin_user)):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    data = payload.model_dump(exclude_unset=True, exclude_none=True)
    if "first_name" in data or "last_name" in data:
        data["name"] = data.pop("name", employee.name)
        first_name = data.pop("first_name", employee.first_name)
        last_name = data.pop("last_name", employee.last_name)
        data["name"] = f"{first_name} {last_name}".strip()
    if "hire_date" in data:
        data["joining_date"] = data.pop("hire_date")
    data.pop("position", None)
    for key, value in data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    await manager.broadcast("employees.updated")
    return employee_response(employee)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, db: Session = Depends(get_db), _admin=Depends(admin_user)):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    await manager.broadcast("employees.updated")
    return {"message": "Employee deleted"}
