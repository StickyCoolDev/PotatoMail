@echo off
REM Setup script for PotatoMail Appwrite collections (Windows)
REM This script validates the environment and runs the Python setup script

setlocal enabledelayedexpansion

echo ==================================
echo PotatoMail Appwrite Setup
echo ==================================

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo Error: .env file not found
    echo.
    echo Please copy .env.example to .env and fill in your Appwrite credentials:
    echo   copy .env.example .env
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo.
echo Checking dependencies...
python -c "import appwrite" 2>nul
if errorlevel 1 (
    echo Appwrite SDK not found. Installing dependencies...
    uv sync
)

REM Run the setup script
echo.
echo Running Appwrite collections setup...
uv run python setup_appwrite.py

if errorlevel 1 (
    echo.
    echo Setup failed. Press any key to exit.
    pause
    exit /b 1
)

echo.
echo Setup complete! Press any key to exit.
pause
