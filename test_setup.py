#!/usr/bin/env python3
"""
Simple test script to verify AgroMarket setup
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

def test_imports():
    """Test that all apps can be imported."""
    print("Testing imports...")
    
    try:
        from core import models as core_models
        from users import models as user_models
        from marketplace import models as marketplace_models
        from forum import models as forum_models
        from cart import models as cart_models
        from insights import models as insights_models
        print("✓ All app models imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection."""
    print("Testing database connection...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] == 1:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
    
    return False

def test_models():
    """Test that models are properly configured."""
    print("Testing models...")
    
    try:
        from users.models import User
        from marketplace.models import Category, Product
        from forum.models import ForumCategory, Thread
        
        # Test model creation (without saving)
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        category = Category(
            name='Test Category',
            description='Test description'
        )
        
        forum_category = ForumCategory(
            name='Test Forum Category',
            description='Test forum description'
        )
        
        print("✓ Models can be instantiated")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_urls():
    """Test URL configuration."""
    print("Testing URL configuration...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Test some basic URLs
        urls_to_test = [
            'core:home',
            'users:login',
            'users:register',
            'marketplace:product_list',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"  ✓ {url_name} -> {url}")
            except Exception as e:
                print(f"  ✗ {url_name} failed: {e}")
                return False
        
        print("✓ URL configuration is valid")
        return True
    except Exception as e:
        print(f"✗ URL test failed: {e}")
        return False

def test_static_files():
    """Test static files configuration."""
    print("Testing static files...")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        # Test that main CSS and JS files exist
        static_files = [
            'css/tailwind.css',
            'css/main.css',
            'js/main.js'
        ]
        
        for static_file in static_files:
            file_path = find(static_file)
            if file_path:
                print(f"  ✓ Found {static_file}")
            else:
                print(f"  ✗ Missing {static_file}")
        
        print("✓ Static files configuration tested")
        return True
    except Exception as e:
        print(f"✗ Static files test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("AgroMarket Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_connection,
        test_models,
        test_urls,
        test_static_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your AgroMarket setup is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)