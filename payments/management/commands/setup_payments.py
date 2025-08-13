from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from payments.models import PaymentMethod, UserBalance
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up default payment methods and user balances for AgroMarket'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Setting up AgroMarket Payment System...")
        
        # Create default payment methods
        payment_methods_data = [
            {
                'name': 'Credit Card',
                'payment_type': 'credit_card',
                'description': 'Secure credit card payments with SSL encryption',
                'processing_fee_percentage': Decimal('2.9'),
                'processing_fee_fixed': Decimal('0.30'),
                'icon_class': 'fas fa-credit-card'
            },
            {
                'name': 'PayPal',
                'payment_type': 'paypal',
                'description': 'Fast and secure PayPal payments',
                'processing_fee_percentage': Decimal('2.9'),
                'processing_fee_fixed': Decimal('0.30'),
                'icon_class': 'fab fa-paypal'
            },
            {
                'name': 'Account Balance',
                'payment_type': 'account_balance',
                'description': 'Use your AgroMarket account balance',
                'processing_fee_percentage': Decimal('0.0'),
                'processing_fee_fixed': Decimal('0.00'),
                'icon_class': 'fas fa-wallet'
            }
        ]
        
        for method_data in payment_methods_data:
            PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            self.stdout.write(f"✅ Payment method: {method_data['name']}")
        
        # Set up user balances
        users = User.objects.all()
        for user in users:
            UserBalance.objects.get_or_create(
                user=user,
                defaults={'amount': Decimal('0.00')}
            )
        
        self.stdout.write("✅ Payment system setup completed!") 