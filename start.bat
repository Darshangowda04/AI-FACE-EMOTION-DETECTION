@echo off
REM Windows Startup Script for Emotion Detection

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   AI Face Emotion Detection - Setup & Start           ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python found

REM Check if venv exists
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements installed
pip show deepface >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies (this may take a few minutes)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
)

echo.
echo ═══════════════════════════════════════════════════════
echo          Ready to start emotion detection!
echo ═══════════════════════════════════════════════════════
echo.
echo Choose an option:
echo   1 - Run real-time emotion detection app
echo   2 - Start REST API server
echo   3 - Run examples
echo   4 - View quick start guide
echo   5 - Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    cls
    echo Starting real-time emotion detection...
    echo.
    python app.py
) else if "%choice%"=="2" (
    cls
    echo Starting REST API server...
    echo Open browser at http://localhost:5000
    echo.
    python api.py
) else if "%choice%"=="3" (
    cls
    echo Running examples...
    echo.
    python examples.py
) else if "%choice%"=="4" (
    cls
    python QUICKSTART.py
) else (
    echo Goodbye!
)

pause
