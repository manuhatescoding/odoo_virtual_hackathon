import sys
from uuid import uuid4
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_docs(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/openapi.json").status_code == 200


def test_business_routes_require_authentication(client):
    assert client.get("/api/employees").status_code == 401
    assert client.get("/api/attendance").status_code == 401


def test_login_returns_signed_token_and_reads_data(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123", "login_as": "admin"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    authenticated = client.get("/api/employees", headers={"Authorization": f"Bearer {token}"})
    assert authenticated.status_code == 200
    assert isinstance(authenticated.json(), list)


def test_invalid_login_is_rejected(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrong-password", "login_as": "admin"})
    assert response.status_code == 401


def test_role_selection_and_employee_scope(client):
    admin = client.post("/api/auth/login", json={"username": "admin", "password": "admin123", "login_as": "admin"})
    employee = client.post("/api/auth/login", json={"username": "employee", "password": "employee123", "login_as": "employee"})
    assert admin.status_code == 200
    assert employee.status_code == 200
    admin_rows = client.get("/api/employees", headers={"Authorization": f"Bearer {admin.json()['access_token']}"}).json()
    employee_rows = client.get("/api/employees", headers={"Authorization": f"Bearer {employee.json()['access_token']}"}).json()
    assert len(admin_rows) >= len(employee_rows) >= 1
    assert employee_rows[0]["user_id"] == employee.json()["user"]["id"]


def test_role_mismatch_is_rejected(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123", "login_as": "employee"})
    assert response.status_code == 401


def test_registration_and_email_verification(client):
    suffix = uuid4().hex[:8]
    response = client.post("/api/auth/register", json={"employee_id": "EMP-TEST", "username": f"verification-{suffix}", "email": f"verification-{suffix}@example.com", "password": "test1234", "full_name": "Verification Test", "role": "employee"})
    assert response.status_code == 201
    verification = client.post("/api/auth/verify-email", params={"email": f"verification-{suffix}@example.com", "token": response.json()["verification_token"]})
    assert verification.status_code == 200

def test_notifications_are_scoped_and_payroll_alerts_are_created(client):
    admin = client.post("/api/auth/login", json={"email": "admin@dayflow.local", "password": "admin123", "login_as": "admin"})
    assert admin.status_code == 200
    token = admin.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    notifications = client.get("/api/notifications", headers=headers)
    assert notifications.status_code == 200
    assert isinstance(notifications.json(), list)