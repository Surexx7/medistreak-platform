#!/bin/bash
# MediScope Platform Setup Script for Mac/Linux

echo "🚀 Setting up MediScope Platform..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv mediscope_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source mediscope_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create sample data
echo "👥 Creating sample data..."
python scripts/create_student_data.py

echo "✅ Setup complete!"
echo ""
echo "🔑 Login Credentials:"
echo "Admin: admin / admin123"
echo "Demo Student: demo_student / mediscope123"
echo "Other Students: password123"
echo ""
echo "🚀 To start the server:"
echo "source mediscope_env/bin/activate"
echo "python manage.py runserver"
echo ""
echo "🌐 Then visit: http://localhost:8000"
