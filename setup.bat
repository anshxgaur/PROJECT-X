@echo off
REM BiltyBook Intelligence - Quick Start Script for Windows

echo.
echo ================================================
echo BiltyBook Intelligence - Setup ^& Run
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python 3 is not installed. Please install Python 3.10+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [X] Node.js is not installed. Please install Node.js 18+
    pause
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing backend dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo [!] Please edit backend\.env with your PostgreSQL credentials
)

echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo Setting up Frontend...
cd ..\frontend

REM Install dependencies
echo Installing frontend dependencies...
call npm install

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)

echo [OK] Frontend setup complete
echo.

echo ================================================
echo [OK] Setup Complete!
echo ================================================
echo.
echo To run the application:
echo.
echo PowerShell Terminal 1 - Backend:
echo   cd backend
echo   .\venv\Scripts\Activate.ps1
echo   python main.py
echo.
echo PowerShell Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo.
echo API Docs: http://localhost:8000/docs
echo.
pause
