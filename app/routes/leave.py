from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Employee, LeaveRequest, Notification, User
from app.schemas import LeaveCreate
from app.utils.dependencies import admin_user, current_user
from app.services.realtime_service import manager

router = APIRouter(prefix="/api/leave", tags=["leave"], dependencies=[Depends(current_user)])


@router.get("")
def list_leaves(db: Session = Depends(get_db), user=Depends(current_user)):
    query = db.query(LeaveRequest).order_by(LeaveRequest.start_date.desc())
    if user.role != "admin":
        query = query.join(Employee).filter(Employee.user_id == user.id)
    return query.all()


@router.post("", status_code=201)
async def create_leave(payload: LeaveCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=422, detail="End date must be on or after start date")
    if not db.get(Employee, payload.employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = db.get(Employee, payload.employee_id)
    if user.role != "admin" and employee.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only request leave for yourself")
    request = LeaveRequest(**payload.model_dump())
    db.add(request)
    db.commit()
    db.refresh(request)
    employee = db.get(Employee, request.employee_id)
    recipients = [employee.user_id] if employee and employee.user_id else []
    recipients.extend(item.id for item in db.query(User).filter(User.role == "admin").all())
    for user_id in set(recipients):
        db.add(Notification(user_id=user_id, title="Leave request submitted", message=f"Leave request for {employee.name if employee else 'an employee'} is pending review.", category="leave"))
    db.commit()
    await manager.broadcast("leave.updated")
    return request


@router.patch("/{leave_id}/status")
async def update_leave_status(leave_id: int, status: str, admin_comment: str | None = None, db: Session = Depends(get_db), _admin=Depends(admin_user)):
    request = db.get(LeaveRequest, leave_id)
    if not request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if status not in {"Pending", "Approved", "Rejected"}:
        raise HTTPException(status_code=422, detail="Status must be Pending, Approved, or Rejected")
    request.status = status
    request.admin_comment = admin_comment
    db.commit()
    db.refresh(request)
    employee = db.get(Employee, request.employee_id)
    if employee and employee.user_id:
        db.add(Notification(user_id=employee.user_id, title=f"Leave request {status.lower()}", message=f"Your leave request was {status.lower()}. {admin_comment or ''}".strip(), category="leave"))
        db.commit()
    await manager.broadcast("leave.updated")
    return request
