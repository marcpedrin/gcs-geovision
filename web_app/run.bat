@echo off
REM Start GeoVision Campus Security Backend API

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  🎥 GeoVision Campus Security Backend API              ║
echo ║     FastAPI Server                                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Seed database with sample data (optional)
if not exist "gcs.db" (
    echo 🌱 Seeding database with sample data...
    python seed.py
)

REM Start the server
echo.
echo 🚀 Starting FastAPI server on http://127.0.0.1:8000
echo.
echo 📚 API Documentation:
echo    - Swagger UI: http://127.0.0.1:8000/docs
echo    - ReDoc: http://127.0.0.1:8000/redoc
echo    - Health: http://127.0.0.1:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
