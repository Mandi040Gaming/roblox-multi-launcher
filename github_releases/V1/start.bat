@echo off
title Roblox Multi-Account Launcher
color 0A
echo.
echo  =========================================
echo   Roblox Multi-Account Launcher
echo   Starting...
echo  =========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo.
    echo  Please install Python 3.11 or newer from:
    echo  https://www.python.org/downloads/
    echo.
    echo  Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

:: Install dependencies silently
echo  Checking dependencies...
python -m pip install requests cryptography Pillow --quiet --disable-pip-version-check

echo  Launching...
echo.
python roblox_launcher.py

if errorlevel 1 (
    echo.
    echo  [ERROR] Launcher crashed. See error above.
    pause
)
