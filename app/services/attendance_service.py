from sqlalchemy.orm import Session
from app.models import Attendance


def list_records(db: Session):
    return db.query(Attendance).order_by(Attendance.date.desc()).all()
