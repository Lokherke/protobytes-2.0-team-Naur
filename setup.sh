#!/bin/bash

# Insurance AI Agent - Setup Script
# This script sets up the Django project for development

echo "=========================================="
echo "Insurance AI Agent - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create media directory
echo "Creating media directories..."
mkdir -p media/claims/damage_images

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the development server:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate  (Linux/Mac)"
echo "     venv\\Scripts\\activate   (Windows)"
echo ""
echo "  2. Run the server:"
echo "     python manage.py runserver"
echo ""
echo "  3. Open your browser and go to:"
echo "     http://127.0.0.1:8000/"
echo ""
echo "  4. Admin panel:"
echo "     http://127.0.0.1:8000/admin/"
echo ""
echo "To create an admin user, run:"
echo "     python manage.py createsuperuser"
echo ""
