#!/usr/bin/env python3
"""
Script to create sample data for testing cart functionality
"""

import os
import sys
import django
from django.contrib.auth.models import User
from django.db import transaction

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from marketplace.models import Category, Product
from cart.models import Cart, CartItem

def create_sample_data():
    """Create sample data for testing"""
    print("🌱 Creating sample data...")
    
    with transaction.atomic():
        # Create a test user
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
        
        # Create a test category
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
        
        # Create test products
        products_data = [
            {
                'name': 'Fresh Apples',
                'slug': 'fresh-apples',
                'description': 'Sweet and juicy organic apples',
                'price': 2.99,
                'quantity_available': 100,
                'unit': 'lb',
                'location': 'Local Farm'
            },
            {
                'name': 'Organic Carrots',
                'slug': 'organic-carrots',
                'description': 'Fresh organic carrots from local farms',
                'price': 1.99,
                'quantity_available': 50,
                'unit': 'lb',
                'location': 'Local Farm'
            },
            {
                'name': 'Fresh Tomatoes',
                'slug': 'fresh-tomatoes',
                'description': 'Ripe and juicy tomatoes',
                'price': 3.49,
                'quantity_available': 75,
                'unit': 'lb',
                'location': 'Local Farm'
            }
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': category,
                    'seller': user,
                    'quantity_available': product_data['quantity_available'],
                    'unit': product_data['unit'],
                    'location': product_data['location']
                }
            )
            if created:
                print(f"✅ Created product: {product.name}")
            else:
                print(f"✅ Using existing product: {product.name}")
        
        print("\n🎯 Sample data creation completed!")
        print(f"📊 Created/Found: {User.objects.count()} users, {Category.objects.count()} categories, {Product.objects.count()} products")

if __name__ == '__main__':
    create_sample_data() 