from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Attendance, LeaveRequest, Payroll
from app.utils.dependencies import admin_user

router = APIRouter(prefix="/api/reports", tags=["reports"], dependencies=[Depends(admin_user)])


@router.get("/attendance")
def attendance_report(db: Session = Depends(get_db)):
    return {"total": db.query(Attendance).count(), "by_status": dict(db.query(Attendance.status, func.count(Attendance.id)).group_by(Attendance.status).all())}


@router.get("/leave")
def leave_report(db: Session = Depends(get_db)):
    return {"total": db.query(LeaveRequest).count(), "by_status": dict(db.query(LeaveRequest.status, func.count(LeaveRequest.id)).group_by(LeaveRequest.status).all())}


@router.get("/payroll")
def payroll_report(db: Session = Depends(get_db)):
    total = db.query(func.coalesce(func.sum(Payroll.basic_salary + Payroll.allowances - Payroll.deductions), 0)).scalar()
    return {"total_records": db.query(Payroll).count(), "net_payroll": float(total)}
