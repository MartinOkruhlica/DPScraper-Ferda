@echo off
cd /d "%~dp0"

echo Setting up Python environment...

py -m venv .venv

if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Installation complete!
pause

