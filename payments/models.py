from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class PaymentMethod(models.Model):
    """Available payment methods"""
    PAYMENT_TYPES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('mobile_money', 'Mobile Money'),
        ('account_balance', 'Account Balance'),
    ]
    
    name = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    is_active = models.BooleanField(default=True)
    processing_fee_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    processing_fee_fixed = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    min_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.01'),
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    max_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('99999.99'),
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default='fas fa-credit-card')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_payment_type_display()})"
    
    def calculate_fees(self, amount):
        """Calculate processing fees for a given amount"""
        percentage_fee = amount * (self.processing_fee_percentage / Decimal('100'))
        total_fee = percentage_fee + self.processing_fee_fixed
        return total_fee

class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    shipping_address = models.TextField()
    billing_address = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    @property
    def total_with_fees(self):
        """Total including all fees"""
        return self.grand_total

class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('marketplace.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.order.order_number}"

class Payment(models.Model):
    """Payment records"""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    payment_id = models.CharField(max_length=50, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict)
    security_hash = models.CharField(max_length=64, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.customer.username}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = self.generate_payment_id()
        if not self.total_amount:
            self.total_amount = self.amount + self.processing_fee
        super().save(*args, **kwargs)
    
    def generate_payment_id(self):
        """Generate unique payment ID"""
        return f"PAY-{uuid.uuid4().hex[:12].upper()}"
    
    def generate_security_hash(self):
        """Generate security hash for payment validation"""
        import hashlib
        data = f"{self.payment_id}{self.order.order_number}{self.customer.id}{self.amount}"
        return hashlib.sha256(data.encode()).hexdigest()

class UserBalance(models.Model):
    """User account balance for internal payments"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='balance')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount}"
    
    def can_afford(self, amount):
        """Check if user can afford a purchase"""
        return self.amount >= amount
    
    def deduct(self, amount):
        """Deduct amount from balance"""
        if self.can_afford(amount):
            self.amount -= amount
            self.save()
            return True
        return False
    
    def add(self, amount):
        """Add amount to balance"""
        self.amount += amount
        self.save()

class PaymentSecurity(models.Model):
    """Security settings and audit logs"""
    SECURITY_EVENT_TYPES = [
        ('payment_attempt', 'Payment Attempt'),
        ('fraud_detection', 'Fraud Detection'),
        ('suspicious_activity', 'Suspicious Activity'),
        ('rate_limit_exceeded', 'Rate Limit Exceeded'),
        ('ip_blocked', 'IP Blocked'),
    ]
    
    event_type = models.CharField(max_length=30, choices=SECURITY_EVENT_TYPES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    details = models.JSONField(default=dict)
    risk_score = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.event_type} - {self.ip_address} at {self.created_at}"
