from sqlalchemy.orm import Session
from app.models import LeaveRequest


def list_requests(db: Session):
    return db.query(LeaveRequest).order_by(LeaveRequest.start_date.desc()).all()
