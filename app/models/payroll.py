from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Payroll(Base):
    __tablename__ = "payroll"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    basic_salary = Column(Float, nullable=False)
    legacy_salary = Column("salary", Float, nullable=True)
    allowances = Column(Float, default=0.0, nullable=False)
    deductions = Column(Float, default=0.0, nullable=False)
    net_salary = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)
    legacy_pay_date = Column("pay_date", Date, nullable=True)
    employee = relationship("Employee", back_populates="payroll")
