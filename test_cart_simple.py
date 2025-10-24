#!/usr/bin/env python3
"""
Simple test script to verify cart functionality
"""

import requests
import json

def test_cart_endpoints():
    """Test cart endpoints with simple HTTP requests"""
    base_url = "http://127.0.0.1:8000"  # Updated to match the error URL
    
    print("🧪 Testing Cart Endpoints...")
    
    # Test 1: Access cart view (this was causing the decimal error)
    try:
        response = requests.get(f"{base_url}/cart/")
        print(f"✅ Cart view accessible: {response.status_code}")
        if response.status_code == 200:
            print("   🎉 Cart view is working! Decimal error fixed.")
        elif response.status_code == 500:
            print("   ❌ Server error - check Django logs")
        else:
            print(f"   📝 Response: {response.text[:200]}...")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Django is running on 127.0.0.1:8000")
        return
    except Exception as e:
        print(f"❌ Cart view error: {e}")
    
    # Test 2: Test add to cart endpoint
    try:
        data = {
            'product_id': 1,
            'quantity': 2
        }
        response = requests.post(
            f"{base_url}/cart/add/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ Add to cart endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        elif response.status_code == 400:
            print(f"   Response: {response.text}")
        elif response.status_code == 500:
            print("   ❌ Server error - check Django logs")
    except Exception as e:
        print(f"❌ Add to cart error: {e}")
    
    print("\n🎯 Cart endpoint test completed!")
    print("💡 To test fully, you need to:")
    print("   1. Start Django server: python manage.py runserver")
    print("   2. Create sample products in the database")
    print("   3. Test the frontend cart functionality")

if __name__ == '__main__':
    test_cart_endpoints() 