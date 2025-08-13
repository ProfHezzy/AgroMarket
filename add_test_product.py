#!/usr/bin/env python3
"""
Simple script to add a test product to the database
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from users.models import User
from marketplace.models import Category, Product
from cart.models import Cart, CartItem

def add_test_product():
    """Add a test product to the database"""
    print("🌱 Adding test product to database...")
    
    try:
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✅ Created test user: {user.username}")
        else:
            print(f"✅ Using existing test user: {user.username}")
        
        # Get or create a test category
        category, created = Category.objects.get_or_create(
            name='Fresh Produce',
            defaults={
                'slug': 'fresh-produce',
                'description': 'Fresh fruits and vegetables'
            }
        )
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"✅ Using existing category: {category.name}")
        
        # Create a test product
        product, created = Product.objects.get_or_create(
            slug='test-apples',
            defaults={
                'name': 'Test Fresh Apples',
                'description': 'Fresh organic apples for testing the cart functionality',
                'price': 2.99,
                'category': category,
                'seller': user,
                'quantity_available': 100,
                'unit': 'lb',
                'location': 'Test Farm'
            }
        )
        
        if created:
            print(f"✅ Created test product: {product.name} (ID: {product.id})")
            print(f"   Price: ${product.price}")
            print(f"   Available: {product.quantity_available} {product.unit}")
        else:
            print(f"✅ Using existing test product: {product.name} (ID: {product.id})")
        
        print("\n🎯 Test product added successfully!")
        print(f"💡 You can now test the cart with product ID: {product.id}")
        print("   Go to the marketplace and try adding this product to cart!")
        
    except Exception as e:
        print(f"❌ Error adding test product: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_test_product() 