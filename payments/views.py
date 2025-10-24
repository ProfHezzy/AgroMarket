from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import json
import hashlib
import hmac
import time
import logging

from .models import (
    PaymentMethod, Order, OrderItem, Payment, 
    UserBalance, PaymentSecurity
)
from marketplace.models import Product
from cart.models import Cart, CartItem

logger = logging.getLogger(__name__)

class PaymentSecurityMixin:
    """Mixin for payment security features"""
    
    def check_rate_limit(self, user, ip_address):
        """Check if user has exceeded rate limits"""
        recent_attempts = PaymentSecurity.objects.filter(
            user=user,
            event_type='payment_attempt',
            created_at__gte=timezone.now() - timezone.timedelta(minutes=15)
        ).count()
        
        if recent_attempts > 10:  # Max 10 attempts per 15 minutes
            PaymentSecurity.objects.create(
                event_type='rate_limit_exceeded',
                user=user,
                ip_address=ip_address,
                risk_score=80,
                details={'attempts': recent_attempts}
            )
            return False
        return True
    
    def check_fraud_indicators(self, request, amount):
        """Check for potential fraud indicators"""
        risk_score = 0
        fraud_indicators = []
        
        # Check IP address
        ip_address = self.get_client_ip(request)
        suspicious_ips = PaymentSecurity.objects.filter(
            ip_address=ip_address,
            is_blocked=True
        ).exists()
        
        if suspicious_ips:
            risk_score += 50
            fraud_indicators.append('IP address is blocked')
        
        # Check user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if not user_agent or len(user_agent) < 20:
            risk_score += 20
            fraud_indicators.append('Suspicious user agent')
        
        # Check amount patterns
        if amount > 1000:  # High amount
            risk_score += 30
            fraud_indicators.append('High transaction amount')
        
        # Check time patterns (middle of night)
        current_hour = timezone.now().hour
        if 2 <= current_hour <= 5:
            risk_score += 15
            fraud_indicators.append('Unusual transaction time')
        
        return risk_score, fraud_indicators
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def log_security_event(self, event_type, user, ip_address, details=None, risk_score=0):
        """Log security events"""
        PaymentSecurity.objects.create(
            event_type=event_type,
            user=user,
            ip_address=ip_address,
            details=details or {},
            risk_score=risk_score
        )

@method_decorator(login_required, name='dispatch')
class CheckoutView(PaymentSecurityMixin, View):
    """Checkout view for processing orders"""
    
    def get(self, request):
        """Display checkout form"""
        # Check if this is a "Buy Now" request
        buy_now = request.GET.get('buy_now') == 'true'
        product_id = request.GET.get('product_id')
        quantity = int(request.GET.get('quantity', 1))
        
        if buy_now and product_id:
            # Buy Now flow - single product purchase
            try:
                product = Product.objects.get(id=product_id, is_active=True)
                if product.quantity_available < quantity:
                    messages.error(request, f'Only {product.quantity_available} available.')
                    return redirect('marketplace:product_detail', pk=product_id)
                
                # Calculate totals for single product
                subtotal = product.price * quantity
                shipping = Decimal('5.99') if subtotal > 0 else Decimal('0')
                tax = subtotal * Decimal('0.08')  # 8% tax
                total = subtotal + shipping + tax
                
                # Create a mock cart item for display
                class MockCartItem:
                    def __init__(self, product, quantity):
                        self.product = product
                        self.quantity = quantity
                        self.total_price = product.price * quantity
                
                cart_items = [MockCartItem(product, quantity)]
                
            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')
                return redirect('marketplace:product_list')
        else:
            # Regular checkout flow - from cart
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(cart__user=request.user)
            else:
                cart_items = []
            
            if not cart_items.exists():
                messages.error(request, 'Your cart is empty.')
                return redirect('cart:view')
            
            # Calculate totals
            subtotal = sum(item.total_price for item in cart_items)
            shipping = Decimal('5.99') if subtotal > 0 else Decimal('0')
            tax = subtotal * Decimal('0.08')  # 8% tax
            total = subtotal + shipping + tax
        
        # Get available payment methods
        payment_methods = PaymentMethod.objects.filter(is_active=True)
        
        # Get user balance if available
        try:
            user_balance = UserBalance.objects.get(user=request.user)
        except UserBalance.DoesNotExist:
            user_balance = None
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping': shipping,
            'tax': tax,
            'total': total,
            'payment_methods': payment_methods,
            'user_balance': user_balance,
            'buy_now': buy_now,
            'product_id': product_id,
            'quantity': quantity,
        }
        
        return render(request, 'payments/checkout.html', context)
    
    def post(self, request):
        """Process checkout"""
        try:
            data = json.loads(request.body)
            payment_method_id = data.get('payment_method_id')
            use_balance = data.get('use_balance', False)
            
            # Security checks
            ip_address = self.get_client_ip(request)
            if not self.check_rate_limit(request.user, ip_address):
                return JsonResponse({
                    'success': False,
                    'error': 'Rate limit exceeded. Please try again later.'
                }, status=429)
            
            # Get cart items
            cart_items = CartItem.objects.filter(cart__user=request.user)
            if not cart_items.exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Cart is empty.'
                }, status=400)
            
            # Calculate totals
            subtotal = sum(item.total_price for item in cart_items)
            shipping = Decimal('5.99') if subtotal > 0 else Decimal('0')
            tax = subtotal * Decimal('0.08')
            total = subtotal + shipping + tax
            
            # Get payment method
            payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, is_active=True)
            
            # Check if user can afford with balance
            if use_balance:
                try:
                    user_balance = UserBalance.objects.get(user=request.user)
                    if not user_balance.can_afford(total):
                        return JsonResponse({
                            'success': False,
                            'error': 'Insufficient balance.'
                        }, status=400)
                except UserBalance.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'No account balance available.'
                    }, status=400)
            
            # Fraud detection
            risk_score, fraud_indicators = self.check_fraud_indicators(request, total)
            if risk_score > 70:
                self.log_security_event(
                    'fraud_detection',
                    request.user,
                    ip_address,
                    {'risk_score': risk_score, 'indicators': fraud_indicators}
                )
                return JsonResponse({
                    'success': False,
                    'error': 'Transaction flagged for security review.'
                }, status=403)
            
            # Create order
            with transaction.atomic():
                order = Order.objects.create(
                    customer=request.user,
                    total_amount=subtotal,
                    shipping_fee=shipping,
                    tax_amount=tax,
                    grand_total=total,
                    shipping_address=data.get('shipping_address', ''),
                    billing_address=data.get('billing_address', ''),
                    notes=data.get('notes', '')
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.product.price,
                        total_price=cart_item.total_price
                    )
                
                # Process payment
                if use_balance:
                    # Use account balance
                    user_balance.deduct(total)
                    payment = Payment.objects.create(
                        order=order,
                        customer=request.user,
                        payment_method=payment_method,
                        amount=total,
                        processing_fee=Decimal('0.00'),
                        total_amount=total,
                        status='completed',
                        transaction_id=f"BAL-{int(time.time())}",
                        ip_address=ip_address,
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        security_hash=order.generate_order_number()
                    )
                    
                    # Clear cart
                    cart_items.delete()
                    
                    return JsonResponse({
                        'success': True,
                        'order_number': order.order_number,
                        'message': 'Order placed successfully using account balance!'
                    })
                else:
                    # External payment processing
                    payment = Payment.objects.create(
                        order=order,
                        customer=request.user,
                        payment_method=payment_method,
                        amount=total,
                        processing_fee=payment_method.calculate_fees(total),
                        total_amount=total + payment_method.calculate_fees(total),
                        status='pending',
                        ip_address=ip_address,
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        security_hash=order.generate_order_number()
                    )
                    
                    # Log payment attempt
                    self.log_security_event(
                        'payment_attempt',
                        request.user,
                        ip_address,
                        {'order_id': order.id, 'amount': str(total)}
                    )
                    
                    # Redirect to payment gateway
                    return JsonResponse({
                        'success': True,
                        'payment_id': payment.payment_id,
                        'redirect_url': self.get_payment_gateway_url(payment)
                    })
                    
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid request data.'
            }, status=400)
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred during checkout.'
            }, status=500)
    
    def get_payment_gateway_url(self, payment):
        """Get payment gateway URL based on payment method"""
        # This would integrate with actual payment gateways
        # For now, return a demo URL
        return f"/payments/process/{payment.payment_id}/"

@method_decorator(login_required, name='dispatch')
class BuyNowView(PaymentSecurityMixin, View):
    """Buy Now view for immediate purchase"""
    
    def post(self, request, product_id):
        """Process immediate purchase"""
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            payment_method_id = data.get('payment_method_id')
            use_balance = data.get('use_balance', False)
            
            # Get product
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            # Check availability
            if product.quantity_available < quantity:
                return JsonResponse({
                    'success': False,
                    'error': f'Only {product.quantity_available} available.'
                }, status=400)
            
            # Security checks
            ip_address = self.get_client_ip(request)
            if not self.check_rate_limit(request.user, ip_address):
                return JsonResponse({
                    'success': False,
                    'error': 'Rate limit exceeded. Please try again later.'
                }, status=429)
            
            # Calculate totals
            subtotal = product.price * quantity
            shipping = Decimal('5.99') if subtotal > 0 else Decimal('0')
            tax = subtotal * Decimal('0.08')
            total = subtotal + shipping + tax
            
            # Get payment method
            payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, is_active=True)
            
            # Check balance if using account balance
            if use_balance:
                try:
                    user_balance = UserBalance.objects.get(user=request.user)
                    if not user_balance.can_afford(total):
                        return JsonResponse({
                            'success': False,
                            'error': 'Insufficient balance.'
                        }, status=400)
                except UserBalance.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'No account balance available.'
                    }, status=400)
            
            # Fraud detection
            risk_score, fraud_indicators = self.check_fraud_indicators(request, total)
            if risk_score > 70:
                self.log_security_event(
                    'fraud_detection',
                    request.user,
                    ip_address,
                    {'risk_score': risk_score, 'indicators': fraud_indicators}
                )
                return JsonResponse({
                    'success': False,
                    'error': 'Transaction flagged for security review.'
                }, status=403)
            
            # Create order
            with transaction.atomic():
                order = Order.objects.create(
                    customer=request.user,
                    total_amount=subtotal,
                    shipping_fee=shipping,
                    tax_amount=tax,
                    grand_total=total,
                    shipping_address=data.get('shipping_address', ''),
                    billing_address=data.get('billing_address', ''),
                    notes=data.get('notes', '')
                )
                
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    total_price=subtotal
                )
                
                # Update product quantity
                product.quantity_available -= quantity
                product.save()
                
                # Process payment
                if use_balance:
                    # Use account balance
                    user_balance.deduct(total)
                    payment = Payment.objects.create(
                        order=order,
                        customer=request.user,
                        payment_method=payment_method,
                        amount=total,
                        processing_fee=Decimal('0.00'),
                        total_amount=total,
                        status='completed',
                        transaction_id=f"BAL-{int(time.time())}",
                        ip_address=ip_address,
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        security_hash=order.generate_order_number()
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'order_number': order.order_number,
                        'message': 'Purchase completed successfully using account balance!'
                    })
                else:
                    # External payment processing
                    payment = Payment.objects.create(
                        order=order,
                        customer=request.user,
                        payment_method=payment_method,
                        amount=total,
                        processing_fee=payment_method.calculate_fees(total),
                        total_amount=total + payment_method.calculate_fees(total),
                        status='pending',
                        ip_address=ip_address,
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        security_hash=order.generate_order_number()
                    )
                    
                    # Log payment attempt
                    self.log_security_event(
                        'payment_attempt',
                        request.user,
                        ip_address,
                        {'order_id': order.id, 'amount': str(total)}
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'payment_id': payment.payment_id,
                        'redirect_url': self.get_payment_gateway_url(payment)
                    })
                    
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid request data.'
            }, status=400)
        except Exception as e:
            logger.error(f"Buy Now error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred during purchase.'
            }, status=500)
    
    def get_payment_gateway_url(self, payment):
        """Get payment gateway URL"""
        return f"/payments/process/{payment.payment_id}/"

@method_decorator(login_required, name='dispatch')
class PaymentProcessView(View):
    """Process external payments"""
    
    def get(self, request, payment_id):
        """Display payment processing page"""
        payment = get_object_or_404(Payment, payment_id=payment_id, customer=request.user)
        
        if payment.status != 'pending':
            messages.error(request, 'Payment is not pending.')
            return redirect('payments:order_detail', order_id=payment.order.id)
        
        context = {
            'payment': payment,
            'order': payment.order
        }
        
        return render(request, 'payments/process.html', context)

@csrf_exempt
@require_POST
def payment_webhook(request, payment_id):
    """Handle payment gateway webhooks"""
    try:
        payment = get_object_or_404(Payment, payment_id=payment_id)
        
        # Verify webhook signature (implement based on payment gateway)
        if not verify_webhook_signature(request):
            return HttpResponseForbidden('Invalid signature')
        
        # Process webhook data
        data = json.loads(request.body)
        
        if data.get('status') == 'completed':
            payment.status = 'completed'
            payment.transaction_id = data.get('transaction_id', '')
            payment.gateway_response = data
            payment.save()
            
            # Update order status
            payment.order.status = 'confirmed'
            payment.order.save()
            
            # Clear cart if this was a checkout
            if hasattr(payment.order, 'cart'):
                payment.order.cart.items.all().delete()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return JsonResponse({'success': False}, status=500)

def verify_webhook_signature(request):
    """Verify webhook signature (implement based on payment gateway)"""
    # This would implement actual signature verification
    # For demo purposes, return True
    return True

@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    context = {
        'order': order,
        'payments': order.payments.all()
    }
    
    return render(request, 'payments/order_detail.html', context)

@login_required
def order_list(request):
    """Display user's orders"""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    
    return render(request, 'payments/order_list.html', context)
