import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Employee, User
from app.schemas import UserCreate, UserLogin
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


def public_user(user: User):
    return {"id": user.id, "username": user.username, "email": user.email, "full_name": user.full_name, "role": user.role, "employee_id": user.employee_id, "email_verified": user.email_verified}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise HTTPException(status_code=409, detail="Username or email already registered")
    requested_role = payload.role if payload.role in {"employee", "admin"} else "employee"
    verification_token = secrets.token_urlsafe(32)
    user = User(username=payload.username, email=payload.email, password_hash=hash_password(payload.password), full_name=payload.full_name, role=requested_role, email_verification_token=verification_token)
    db.add(user)
    db.commit()
    db.refresh(user)
    names = payload.full_name.split(" ", 1)
    employee = Employee(user_id=user.id, name=payload.full_name, legacy_first_name=names[0], legacy_last_name=names[1] if len(names) > 1 else "", job_title="Employee", department="General")
    db.add(employee)
    db.commit()
    user.employee_id = employee.id
    db.commit()
    return {**public_user(user), "verification_token": verification_token}


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first()
    requested_role = "admin" if payload.login_as == "admin" else "employee"
    if not user or not verify_password(payload.password, user.password_hash) or user.role != requested_role or not user.email_verified:
        raise HTTPException(status_code=401, detail="Invalid username, password, or login role")
    return {"access_token": create_access_token(user.id, user.role), "token_type": "bearer", "user": public_user(user)}


@router.post("/verify-email")
def verify_email(email: str, token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.email_verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    user.email_verified = True
    user.email_verification_token = None
    db.commit()
    return {"message": "Email verified", "user": public_user(user)}
