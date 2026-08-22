from sqlalchemy.orm import Session
from app.models import Payroll


def list_records(db: Session):
    return db.query(Payroll).order_by(Payroll.pay_date.desc()).all()
