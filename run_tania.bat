@echo off
title Tania AI Assistant
echo.
echo ============================================================
echo                    Tania AI Assistant
echo ============================================================
echo.
echo Starting Tania...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if the main file exists
if not exist "tania_ai_assistant.py" (
    echo ERROR: tania_ai_assistant.py not found
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)

REM Run Tania
python tania_ai_assistant.py

REM If there was an error, pause so user can see the message
if errorlevel 1 (
    echo.
    echo An error occurred while running Tania.
    echo Check the error message above for details.
    pause
)