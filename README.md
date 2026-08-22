# Dayflow-HRMS

Dayflow is a local HR workspace for employee profiles, attendance, leave approvals, payroll, notifications, and HR reports. The React frontend uses the FastAPI backend through the Vite development proxy.

Dayflow-HRMS is a Human Resource Management System (HRMS) designed to streamline HR processes and improve employee management. This project consists of a frontend built with React and a backend developed in Python.

## Project Structure

The project is organized into the following main directories:

- **frontend/**: Contains the React application.
  - **public/**: Static assets such as images and fonts.
  - **src/**: Source code for the React application.
    - **components/**: Reusable components for the application.
    - **pages/**: Main pages of the application.
    - **services/**: API service files for handling requests.
    - **App.jsx**: Main application component.
    - **main.jsx**: Entry point for the React application.

- **backend/**: Contains the backend application.
  - **app/**: Main application logic.
    - **models/**: Data models for the application.
    - **schemas/**: Data validation schemas.
    - **routes/**: API route definitions.
    - **services/**: Business logic services.
    - **database/**: Database connection files.
    - **utils/**: Utility functions.
    - **main.py**: Entry point for the backend application.

- **database/**: SQL schema for the database.
- **docs/**: Documentation files.
- **requirements.txt**: Python dependencies for the backend.
- **README.md**: Project documentation.
- **.gitignore**: Git ignore file.

## Features

- User authentication and authorization.
- Employee management including attendance and leave tracking.
- Payroll management.
- Reporting features for HR analytics.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd Dayflow-HRMS
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

4. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

## Usage

Copy the example environment files before starting:
```powershell
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

You can edit `backend\.env` and `frontend\.env` to provide your own host,
ports, database URL, CORS origins, API URL, or refresh interval. For example,
set `VITE_REFRESH_INTERVAL_MS=3000` to refresh dashboard data every three seconds.

The simplest Windows startup is:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run-backend.ps1
```
Then open a second terminal and run:
```powershell
.\run-frontend.ps1
```

Alternatively, use the commands below.

Start the backend from the repository root:
```powershell
python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --reload --port 8000
```

In a second terminal, start the frontend:
```powershell
cd frontend
npm run dev -- --host 0.0.0.0
```

The frontend runs at `http://127.0.0.1:5173` and the backend API and Swagger docs
are available at `http://127.0.0.1:8000` and `http://127.0.0.1:8000/docs`.

The backend uses SQLite and creates `dayflow.db` automatically. A demo admin
account is available with username `admin` and password `admin123`.

An employee demo account is also available with username `employee` and password
`employee123`. Select the matching `Employee` or `Admin / HR` login option; the
backend rejects role mismatches and limits employee records to the signed-in
employee.

The API uses signed, expiring bearer tokens. Business endpoints require the
token returned by `/api/auth/login`; leave approval and rejection additionally
require the `admin` role. The dashboard includes inputs for creating employees,
submitting leave, creating payroll records, checking out attendance records,
approving or rejecting leave, viewing FAQs, and reading notifications. Payroll
publication and leave decisions notify the affected employee.

## Docker Deployment

Build and run the production stack:
```powershell
docker compose up --build -d
```

Open `http://localhost:5173`. The frontend Nginx server proxies `/api` requests
to the backend container, and the SQLite database is stored in the persistent
`dayflow_data` volume. Stop the stack with:
```powershell
docker compose down
```

## Testing

Run the backend tests from the repository root:
```powershell
python -m pytest backend/tests -q
```

The suite covers health/docs, protected routes, both role logins, employee data
isolation, successful token login, data access, and invalid credentials.

Run the frontend test:
```powershell
npm.cmd --prefix frontend test
```

The production build can be checked with `npm.cmd --prefix frontend run build`.

The frontend test verifies the fresh-session login screen. Push updates use the
authenticated `/ws/updates` WebSocket channel, with polling retained as a fallback.
