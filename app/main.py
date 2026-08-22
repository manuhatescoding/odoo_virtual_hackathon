import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import Base, SessionLocal, engine
from app.database.database import init_db
from app.models import Employee, User
from app.routes import auth, employees, attendance, leave, payroll, reports, notifications
from app.utils.security import decode_access_token, hash_password
from app.services.realtime_service import manager

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(title="Dayflow HRMS API", version="1.0.0")

init_db()


def seed_demo_user():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            db.add(User(username="admin", email="admin@dayflow.local", password_hash=hash_password("admin123"), full_name="Dayflow Admin", role="admin", email_verified=True))
            db.commit()
        else:
            admin.email_verified = True
            db.commit()
        user = db.query(User).filter(User.username == "employee").first()
        if not user:
            user = User(username="employee", email="employee@dayflow.local", password_hash=hash_password("employee123"), full_name="Demo Employee", role="employee", email_verified=True)
            db.add(user)
            db.commit()
        if not user.employee_id:
            employee = db.query(Employee).filter(Employee.user_id == user.id).first()
            if not employee:
                employee = Employee(user_id=user.id, name=user.full_name, legacy_first_name="Demo", legacy_last_name="Employee", job_title="Product Designer", department="Design")
                db.add(employee)
                db.commit()
            user.employee_id = employee.id
            db.add(employee)
            db.commit()
        user.email_verified = True
        db.commit()
    finally:
        db.close()


seed_demo_user()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(reports.router)
app.include_router(notifications.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dayflow HRMS API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.websocket("/ws/updates")
async def updates(websocket: WebSocket):
    token = websocket.query_params.get("token")
    try:
        decode_access_token(token or "")
    except ValueError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)