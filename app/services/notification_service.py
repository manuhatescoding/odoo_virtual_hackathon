from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Attendance, LeaveRequest, Payroll


def attendance_report(db: Session):
    return {"total": db.query(Attendance).count(), "by_status": dict(db.query(Attendance.status, func.count(Attendance.id)).group_by(Attendance.status).all())}


def leave_report(db: Session):
    return {"total": db.query(LeaveRequest).count(), "by_status": dict(db.query(LeaveRequest.status, func.count(LeaveRequest.id)).group_by(LeaveRequest.status).all())}


def payroll_report(db: Session):
    total = db.query(func.coalesce(func.sum(Payroll.salary - Payroll.deductions), 0)).scalar()
    return {"total_records": db.query(Payroll).count(), "net_payroll": float(total)}
