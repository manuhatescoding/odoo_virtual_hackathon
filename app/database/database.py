from app.database.connection import Base, DATABASE_URL, SessionLocal, engine
from sqlalchemy import inspect, text


def init_db():
    migrate_legacy_sqlite_schema()
    Base.metadata.create_all(bind=engine)


def migrate_legacy_sqlite_schema():
    if not DATABASE_URL.startswith("sqlite"):
        return
    with engine.begin() as connection:
        tables = {table[0] for table in connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))}
        if "leaves" in tables and "leave_requests" not in tables:
            connection.execute(text("ALTER TABLE leaves RENAME TO leave_requests"))
            tables.remove("leaves")
            tables.add("leave_requests")
        additions = {
            "users": [("employee_id", "INTEGER"), ("email_verified", "BOOLEAN NOT NULL DEFAULT 0"), ("email_verification_token", "VARCHAR(128)")],
            "employees": [("name", "VARCHAR(120) NOT NULL DEFAULT 'Unnamed employee'"), ("phone", "VARCHAR(30)"), ("address", "VARCHAR(255)"), ("profile_picture", "VARCHAR(500)"), ("job_title", "VARCHAR(80) NOT NULL DEFAULT 'Employee'"), ("joining_date", "DATE")],
            "leave_requests": [("remarks", "VARCHAR(500)"), ("admin_comment", "VARCHAR(500)"), ("created_at", "DATETIME")],
            "payroll": [("basic_salary", "FLOAT NOT NULL DEFAULT 0"), ("allowances", "FLOAT NOT NULL DEFAULT 0"), ("net_salary", "FLOAT NOT NULL DEFAULT 0"), ("effective_date", "DATE")],
            "notifications": [("user_id", "INTEGER NOT NULL"), ("title", "VARCHAR(120) NOT NULL"), ("message", "VARCHAR(500) NOT NULL"), ("category", "VARCHAR(30) NOT NULL DEFAULT 'general'"), ("is_read", "BOOLEAN NOT NULL DEFAULT 0"), ("created_at", "DATETIME")],
        }
        for table, columns in additions.items():
            if table not in tables:
                continue
            existing = {column[1] for column in connection.execute(text(f"PRAGMA table_info({table})"))}
            for name, definition in columns:
                if name not in existing:
                    connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {definition}"))
        if "employees" in tables:
            connection.execute(text("UPDATE employees SET name = trim(coalesce(first_name, '') || ' ' || coalesce(last_name, '')) WHERE name = 'Unnamed employee' OR name IS NULL"))
            connection.execute(text("UPDATE employees SET name = 'Unnamed employee' WHERE name = ''"))
            connection.execute(text("UPDATE employees SET job_title = position WHERE position IS NOT NULL AND (job_title = 'Employee' OR job_title IS NULL)"))
            connection.execute(text("UPDATE employees SET joining_date = hire_date WHERE joining_date IS NULL AND hire_date IS NOT NULL"))
            if "users" in tables:
                connection.execute(text("UPDATE users SET employee_id = employees.id FROM employees WHERE users.id = employees.user_id AND users.employee_id IS NULL"))
        if "payroll" in tables:
            connection.execute(text("UPDATE payroll SET basic_salary = salary WHERE basic_salary = 0 AND salary IS NOT NULL"))
            connection.execute(text("UPDATE payroll SET net_salary = basic_salary + allowances - deductions WHERE net_salary = 0"))
            connection.execute(text("UPDATE payroll SET effective_date = pay_date WHERE effective_date IS NULL AND pay_date IS NOT NULL"))


def get_session():
    return SessionLocal()
