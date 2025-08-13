from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from decimal import Decimal
import random

from marketplace.models import Category, Product

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=20,
            help='Number of products to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Create superuser
        self.create_superuser()
        
        # Create categories
        self.create_categories()
        
        # Create users
        self.create_users(options['users'])
        
        # Create products
        self.create_products(options['products'])
        
        self.stdout.write(self.style.SUCCESS('Database population completed!'))

    def create_superuser(self):
        """Create a superuser if it doesn't exist."""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@agromarket.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin123'))

    def create_categories(self):
        """Create product categories."""
        categories_data = [
            {
                'name': 'Fresh Produce',
                'description': 'Fresh fruits and vegetables'
            },
            {
                'name': 'Grains & Cereals',
                'description': 'Rice, wheat, corn and other grains'
            },
            {
                'name': 'Dairy Products',
                'description': 'Milk, cheese, yogurt and dairy items'
            },
            {
                'name': 'Seeds & Plants',
                'description': 'Seeds, seedlings and plants'
            },
            {
                'name': 'Farming Equipment',
                'description': 'Tools and equipment for farming'
            }
        ]
        
        for cat_data in categories_data:
            slug = slugify(cat_data['name'])
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slug,
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

    def create_users(self, count):
        """Create sample users."""
        users_data = [
            {'first': 'John', 'last': 'Smith', 'role': 'farmer'},
            {'first': 'Jane', 'last': 'Johnson', 'role': 'buyer'},
            {'first': 'Mike', 'last': 'Williams', 'role': 'farmer'},
            {'first': 'Sarah', 'last': 'Brown', 'role': 'seller'},
            {'first': 'David', 'last': 'Jones', 'role': 'buyer'},
            {'first': 'Lisa', 'last': 'Garcia', 'role': 'farmer'},
            {'first': 'Tom', 'last': 'Miller', 'role': 'seller'},
            {'first': 'Emma', 'last': 'Davis', 'role': 'buyer'},
            {'first': 'Chris', 'last': 'Rodriguez', 'role': 'farmer'},
            {'first': 'Anna', 'last': 'Martinez', 'role': 'seller'},
        ]
        
        for i in range(min(count, len(users_data))):
            user_data = users_data[i]
            username = f"{user_data['first'].lower()}{user_data['last'].lower()}"
            email = f"{username}@example.com"
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=user_data['first'],
                    last_name=user_data['last']
                )
                self.stdout.write(f'Created user: {user.username} ({user_data["role"]})')

    def create_products(self, count):
        """Create sample products."""
        categories = list(Category.objects.all())
        users = list(User.objects.filter(is_superuser=False))
        
        if not categories:
            self.stdout.write(self.style.WARNING('No categories found. Skipping product creation.'))
            return
            
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Skipping product creation.'))
            return
        
        product_names = [
            'Organic Tomatoes', 'Fresh Carrots', 'Green Lettuce', 'Red Apples', 'Bananas',
            'Brown Rice', 'Wheat Flour', 'Corn Kernels', 'Fresh Milk', 'Cheddar Cheese',
            'Tomato Seeds', 'Sunflower Seeds', 'Herb Seedlings', 'Tractor Parts', 'Fertilizer'
        ]
        
        units = ['kg', 'lb', 'piece', 'dozen', 'bag', 'box']
        
        for i in range(min(count, len(product_names))):
            category = random.choice(categories)
            seller = random.choice(users)
            name = product_names[i]
            slug = slugify(name)
            
            # Make slug unique if it already exists
            if Product.objects.filter(slug=slug).exists():
                slug = f"{slug}-{i}"
            
            product = Product.objects.create(
                seller=seller,
                category=category,
                name=name,
                slug=slug,
                description=f"High quality {name.lower()}. Fresh and organic, perfect for your needs.",
                price=Decimal(str(round(random.uniform(5.0, 100.0), 2))),
                unit=random.choice(units),
                quantity_available=random.randint(1, 100),
                location=f"Farm {i+1}",
                is_active=True
            )
            
            self.stdout.write(f'Created product: {product.name}')