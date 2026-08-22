from sqlalchemy.orm import Session
from app.models import User
from app.utils.security import hash_password, verify_password


def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    return user if user and verify_password(password, user.password_hash) else None


def create_user(db: Session, username: str, email: str, password: str, full_name: str, role: str = "employee"):
    user = User(username=username, email=email, password_hash=hash_password(password), full_name=full_name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
