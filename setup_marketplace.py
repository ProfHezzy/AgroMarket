#!/usr/bin/env python3
"""
Comprehensive setup script for the AgroMarket marketplace
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

def setup_marketplace():
    """Set up the complete marketplace with categories and products"""
    print("🚀 Setting up AgroMarket Marketplace...")
    print("=" * 50)
    
    try:
        # Step 1: Create test user
        print("\n👤 Step 1: Setting up test user...")
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
        
        # Step 2: Create categories
        print("\n📂 Step 2: Setting up product categories...")
        categories_data = [
            {
                'name': 'Fresh Fruits',
                'slug': 'fresh-fruits',
                'description': 'Fresh, seasonal fruits from local farms'
            },
            {
                'name': 'Fresh Vegetables',
                'slug': 'fresh-vegetables', 
                'description': 'Organic vegetables grown with care'
            },
            {
                'name': 'Grains & Cereals',
                'slug': 'grains-cereals',
                'description': 'Quality grains and cereals for your kitchen'
            },
            {
                'name': 'Dairy & Eggs',
                'slug': 'dairy-eggs',
                'description': 'Fresh dairy products and farm eggs'
            },
            {
                'name': 'Farming Equipment',
                'slug': 'farming-equipment',
                'description': 'Tools and equipment for modern farming'
            },
            {
                'name': 'Seeds & Plants',
                'slug': 'seeds-plants',
                'description': 'High-quality seeds and starter plants'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                print(f"✅ Created category: {category.name}")
            else:
                print(f"✅ Using existing category: {category.name}")
            categories[cat_data['slug']] = category
        
        # Step 3: Create products
        print("\n🛍️ Step 3: Adding products to the marketplace...")
        products_data = [
            # Fresh Fruits
            {
                'name': 'Organic Red Apples',
                'slug': 'organic-red-apples',
                'description': 'Sweet and crisp organic red apples, perfect for eating fresh or baking. Grown without pesticides.',
                'price': 3.99,
                'category': categories['fresh-fruits'],
                'seller': user,
                'quantity_available': 150,
                'unit': 'lb',
                'location': 'Green Valley Farm'
            },
            {
                'name': 'Fresh Strawberries',
                'slug': 'fresh-strawberries',
                'description': 'Juicy, ripe strawberries picked at peak freshness. Perfect for desserts or eating fresh.',
                'price': 5.99,
                'category': categories['fresh-fruits'],
                'seller': user,
                'quantity_available': 80,
                'unit': 'lb',
                'location': 'Berry Hill Farm'
            },
            {
                'name': 'Sweet Oranges',
                'slug': 'sweet-oranges',
                'description': 'Large, sweet oranges with thin skin. High in vitamin C and perfect for juicing.',
                'price': 2.49,
                'category': categories['fresh-fruits'],
                'seller': user,
                'quantity_available': 200,
                'unit': 'lb',
                'location': 'Citrus Grove Farm'
            },
            
            # Fresh Vegetables
            {
                'name': 'Organic Carrots',
                'slug': 'organic-carrots',
                'description': 'Fresh organic carrots, sweet and crunchy. Perfect for salads, soups, or snacking.',
                'price': 2.99,
                'category': categories['fresh-vegetables'],
                'seller': user,
                'quantity_available': 120,
                'unit': 'lb',
                'location': 'Root Valley Farm'
            },
            {
                'name': 'Fresh Tomatoes',
                'slug': 'fresh-tomatoes',
                'description': 'Ripe, juicy tomatoes perfect for salads, sandwiches, or cooking. Grown in rich soil.',
                'price': 3.49,
                'category': categories['fresh-vegetables'],
                'seller': user,
                'quantity_available': 100,
                'unit': 'lb',
                'location': 'Sunny Side Farm'
            },
            {
                'name': 'Green Bell Peppers',
                'slug': 'green-bell-peppers',
                'description': 'Crisp green bell peppers, great for stuffing, salads, or cooking. Mild and versatile.',
                'price': 2.79,
                'category': categories['fresh-vegetables'],
                'seller': user,
                'quantity_available': 90,
                'unit': 'lb',
                'location': 'Pepper Patch Farm'
            },
            
            # Grains & Cereals
            {
                'name': 'Organic Brown Rice',
                'slug': 'organic-brown-rice',
                'description': 'Nutritious organic brown rice, rich in fiber and minerals. Perfect for healthy meals.',
                'price': 4.99,
                'category': categories['grains-cereals'],
                'seller': user,
                'quantity_available': 300,
                'unit': 'lb',
                'location': 'Golden Grain Farm'
            },
            {
                'name': 'Whole Wheat Flour',
                'slug': 'whole-wheat-flour',
                'description': 'Freshly milled whole wheat flour, perfect for bread baking and healthy cooking.',
                'price': 3.79,
                'category': categories['grains-cereals'],
                'seller': user,
                'quantity_available': 250,
                'unit': 'lb',
                'location': 'Mill Creek Farm'
            },
            
            # Dairy & Eggs
            {
                'name': 'Farm Fresh Eggs',
                'slug': 'farm-fresh-eggs',
                'description': 'Large, farm-fresh eggs from free-range chickens. Rich yolks and excellent flavor.',
                'price': 4.99,
                'category': categories['dairy-eggs'],
                'seller': user,
                'quantity_available': 50,
                'unit': 'dozen',
                'location': 'Happy Hen Farm'
            },
            {
                'name': 'Fresh Whole Milk',
                'slug': 'fresh-whole-milk',
                'description': 'Creamy whole milk from grass-fed cows. Rich and nutritious, perfect for drinking or cooking.',
                'price': 6.99,
                'category': categories['dairy-eggs'],
                'seller': user,
                'quantity_available': 40,
                'unit': 'gallon',
                'location': 'Dairy Delight Farm'
            },
            
            # Farming Equipment
            {
                'name': 'Garden Trowel Set',
                'slug': 'garden-trowel-set',
                'description': 'Professional grade garden trowel set with ergonomic handles. Perfect for planting and weeding.',
                'price': 24.99,
                'category': categories['farming-equipment'],
                'seller': user,
                'quantity_available': 25,
                'unit': 'set',
                'location': 'Tool Time Supply'
            },
            {
                'name': 'Watering Can',
                'slug': 'watering-can',
                'description': 'Large capacity watering can with fine rose attachment. Ideal for gentle plant watering.',
                'price': 19.99,
                'category': categories['farming-equipment'],
                'seller': user,
                'quantity_available': 30,
                'unit': 'piece',
                'location': 'Tool Time Supply'
            },
            
            # Seeds & Plants
            {
                'name': 'Tomato Seed Packets',
                'slug': 'tomato-seed-packets',
                'description': 'Heirloom tomato seeds with detailed growing instructions. Multiple varieties included.',
                'price': 8.99,
                'category': categories['seeds-plants'],
                'seller': user,
                'quantity_available': 100,
                'unit': 'packet',
                'location': 'Seed Success Store'
            },
            {
                'name': 'Herb Starter Plants',
                'slug': 'herb-starter-plants',
                'description': 'Healthy herb starter plants including basil, rosemary, and thyme. Ready to transplant.',
                'price': 12.99,
                'category': categories['seeds-plants'],
                'seller': user,
                'quantity_available': 60,
                'unit': 'set',
                'location': 'Seed Success Store'
            }
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            
            if created:
                created_count += 1
                print(f"✅ Created: {product.name} - ${product.price} ({product.quantity_available} {product.unit})")
            else:
                print(f"✅ Exists: {product.name} - ${product.price} ({product.quantity_available} {product.unit})")
        
        # Step 4: Summary
        print("\n" + "=" * 50)
        print("🎯 MARKETPLACE SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"📊 Database Summary:")
        print(f"   👥 Users: {User.objects.count()}")
        print(f"   📂 Categories: {Category.objects.count()}")
        print(f"   🛍️ Products: {Product.objects.count()}")
        print(f"   🌱 New products added: {created_count}")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Start Django server: python manage.py runserver")
        print(f"   2. Go to: http://127.0.0.1:8000/marketplace/")
        print(f"   3. Test the cart functionality by adding products")
        print(f"   4. View your cart at: http://127.0.0.1:8000/cart/")
        
        print(f"\n🔑 Test Account:")
        print(f"   Username: testuser")
        print(f"   Password: testpass123")
        
        print(f"\n✨ Your marketplace is now ready with realistic agricultural products!")
        
    except Exception as e:
        print(f"❌ Error setting up marketplace: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_marketplace() 