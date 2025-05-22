@echo off
echo Installing Crymson dependencies...
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or newer.
    echo You can download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing required packages...
pip install customtkinter==5.2.1
pip install requests==2.31.0

echo.
echo Installation complete! You can now run Crymson by double-clicking run.bat
echo.
pause 