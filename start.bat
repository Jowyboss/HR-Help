@echo off
REM HR Help Desk - Quick Start Script for Windows
REM This script sets up and runs the HR Help Desk application with SQLite

echo.
echo HR Help Desk - Quick Start Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Found Python
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Step 1: Install dependencies
echo Step 1: Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt -q
cd ..

REM Step 2: Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Step 2: Creating .env configuration...
    (
        echo SECRET_KEY=dev-secret-key-change-in-production
        echo DATABASE_TYPE=sqlite
        echo DATABASE_NAME=hr_helpdesk
        echo FLASK_ENV=development
    ) > .env
    echo [OK] Created .env file
) else (
    echo.
    echo [OK] Using existing .env file
)

REM Step 3: Set up database with sample data
echo.
echo Step 3: Setting up database with sample data...
cd backend
python populate_db.py
cd ..

REM Step 4: Instructions
echo.
echo ====================================
echo Setup complete!
echo ====================================
echo.
echo The application is ready to run.
echo.
echo Opening backend server in a new window...
start "HR Help Desk - Backend" cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak >nul

echo Opening frontend server in a new window...
start "HR Help Desk - Frontend" cmd /k "cd frontend && python -m http.server 8080"
timeout /t 2 /nobreak >nul

echo.
echo ====================================
echo Servers are starting!
echo ====================================
echo.
echo Your browser should open automatically.
echo If not, visit these URLs:
echo.
echo   Submit Ticket: http://localhost:8080/index.html
echo   Dashboard:     http://localhost:8080/dashboard.html
echo   API:           http://localhost:5000/api/tickets
echo.
echo Press any key to open the dashboard in your browser...
pause >nul

start http://localhost:8080/dashboard.html

echo.
echo To stop the servers, close the backend and frontend windows.
echo.
pause
