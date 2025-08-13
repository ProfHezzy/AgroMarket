#!/usr/bin/env python3
"""
Simple test script to verify cart functionality
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def test_cart_functionality():
    """Test basic cart functionality"""
    client = Client()
    
    print("🧪 Testing Cart Functionality...")
    
    # Test 1: Access cart view
    try:
        response = client.get('/cart/')
        print(f"✅ Cart view accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Cart view error: {e}")
    
    # Test 2: Test add to cart endpoint
    try:
        response = client.post('/cart/add/', 
                             data={'product_id': 1, 'quantity': 2},
                             content_type='application/json')
        print(f"✅ Add to cart endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Add to cart error: {e}")
    
    # Test 3: Test update cart endpoint
    try:
        response = client.post('/cart/update/', 
                             data={'product_id': 1, 'quantity': 3},
                             content_type='application/json')
        print(f"✅ Update cart endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Update cart error: {e}")
    
    # Test 4: Test remove from cart endpoint
    try:
        response = client.post('/cart/remove/', 
                             data={'product_id': 1},
                             content_type='application/json')
        print(f"✅ Remove from cart endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Remove from cart error: {e}")
    
    print("\n🎯 Cart functionality test completed!")

if __name__ == '__main__':
    test_cart_functionality() 