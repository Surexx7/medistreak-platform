@echo off
REM MediScope Platform Setup Script for Windows

echo 🚀 Setting up MediScope Platform...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv mediscope_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call mediscope_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗄️  Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create sample data
echo 👥 Creating sample data...
python scripts/create_student_data.py

echo ✅ Setup complete!
echo.
echo 🔑 Login Credentials:
echo Admin: admin / admin123
echo Demo Student: demo_student / mediscope123
echo Other Students: password123
echo.
echo 🚀 To start the server:
echo mediscope_env\Scripts\activate
echo python manage.py runserver
echo.
echo 🌐 Then visit: http://localhost:8000
pause
