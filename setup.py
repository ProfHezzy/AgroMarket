#!/usr/bin/env python3
"""
AgroMarket Setup Script
This script helps set up the AgroMarket Django project.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description or command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_requirements():
    """Check if required software is installed."""
    print("Checking requirements...")
    
    requirements = {
        'python': 'python --version',
        'pip': 'pip --version',
        'git': 'git --version'
    }
    
    missing = []
    for name, command in requirements.items():
        if not run_command(command, f"Checking {name}"):
            missing.append(name)
    
    if missing:
        print(f"\nMissing requirements: {', '.join(missing)}")
        print("Please install the missing requirements and try again.")
        return False
    
    return True

def setup_environment():
    """Set up the development environment."""
    print("\nSetting up development environment...")
    
    # Create .env file from example
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("Created .env file from .env.example")
        print("Please edit .env file with your configuration.")
    
    # Install Python dependencies
    if not run_command('pip install -r requirements.txt', 'Installing Python dependencies'):
        return False
    
    return True

def setup_database():
    """Set up the database."""
    print("\nSetting up database...")
    
    # Run migrations
    if not run_command('python manage.py makemigrations', 'Creating migrations'):
        return False
    
    if not run_command('python manage.py migrate', 'Running migrations'):
        return False
    
    # Populate with sample data
    response = input("\nDo you want to populate the database with sample data? (y/n): ")
    if response.lower() in ['y', 'yes']:
        if not run_command('python manage.py populate_db', 'Populating database with sample data'):
            print("Warning: Failed to populate database with sample data.")
    
    return True

def collect_static():
    """Collect static files."""
    print("\nCollecting static files...")
    return run_command('python manage.py collectstatic --noinput', 'Collecting static files')

def create_superuser():
    """Create a superuser."""
    response = input("\nDo you want to create a superuser? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("Creating superuser...")
        os.system('python manage.py createsuperuser')

def main():
    """Main setup function."""
    print("AgroMarket Setup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("Failed to set up environment.")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("Failed to set up database.")
        sys.exit(1)
    
    # Collect static files
    if not collect_static():
        print("Warning: Failed to collect static files.")
    
    # Create superuser
    create_superuser()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Edit the .env file with your configuration")
    print("2. Start the development server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000 to see your application")
    print("\nDefault superuser (if created via populate_db): admin/admin123")
    print("\nFor production deployment, see the Docker configuration files.")

if __name__ == '__main__':
    main()