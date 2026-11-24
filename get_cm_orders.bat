@echo off
cd /d "C:\Users\Fujitsu\OneDrive\Projects\DPScraper Ferda"

if not exist ".venv\Scripts\python.exe" (
    echo Python environment not found.
    echo Please run install.bat first.
    pause
    exit /b 1
)

.venv\Scripts\python.exe get_cm_orders.py

if errorlevel 1 (
    echo.
    echo Script encountered an error.
    pause
)