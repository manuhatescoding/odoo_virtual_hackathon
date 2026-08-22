from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=True)
    name = Column(String(120), nullable=False, default="Unnamed employee")
    legacy_first_name = Column("first_name", String(50), nullable=True)
    legacy_last_name = Column("last_name", String(50), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)
    profile_picture = Column(String(500), nullable=True)
    job_title = Column(String(80), default="Employee")
    department = Column(String(80), default="General")
    joining_date = Column(Date, default=date.today)
    user = relationship("User", back_populates="employee")
    attendance = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    leaves = relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    payroll = relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")

    @property
    def first_name(self):
        return self.legacy_first_name or self.name.split(" ", 1)[0]

    @property
    def last_name(self):
        return self.legacy_last_name or (self.name.split(" ", 1)[1] if " " in self.name else "")

    @property
    def position(self):
        return self.job_title

    @property
    def hire_date(self):
        return self.joining_date
