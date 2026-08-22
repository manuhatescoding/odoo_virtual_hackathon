from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Attendance, Employee
from app.schemas import AttendanceCreate
from app.utils.dependencies import admin_user, current_user
from app.services.realtime_service import manager

router = APIRouter(prefix="/api/attendance", tags=["attendance"], dependencies=[Depends(current_user)])


@router.get("")
def list_attendance(db: Session = Depends(get_db), user=Depends(current_user)):
    query = db.query(Attendance).order_by(Attendance.date.desc())
    if user.role != "admin":
        query = query.join(Employee).filter(Employee.user_id == user.id)
    return query.all()


@router.post("", status_code=201)
async def create_attendance(payload: AttendanceCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    if not db.get(Employee, payload.employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = db.get(Employee, payload.employee_id)
    if user.role != "admin" and employee.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only record your own attendance")
    record = Attendance(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    await manager.broadcast("attendance.updated")
    return record


@router.patch("/{attendance_id}/checkout")
async def checkout(attendance_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    record = db.get(Attendance, attendance_id)
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    if user.role != "admin" and record.employee.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only check out your own attendance")
    if record.check_out:
        raise HTTPException(status_code=409, detail="Attendance record is already checked out")
    from datetime import datetime
    record.check_out = datetime.utcnow()
    db.commit()
    db.refresh(record)
    await manager.broadcast("attendance.updated")
    return record
