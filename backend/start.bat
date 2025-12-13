@echo off
echo Starting Backend Server...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file from .env.example
    echo.
    pause
)

REM Start server
echo.
echo Starting Flask server...
echo Backend will run on http://localhost:5000
echo.
python app.py

pause

