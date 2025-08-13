from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
import json

from .models import Cart, CartItem
from marketplace.models import Product

def cart_view(request):
    """Shopping cart view"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    else:
        # Handle anonymous users with session-based cart
        cart_items = []
        session_cart = request.session.get('cart', {})
        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price * Decimal(quantity)
                })
            except Product.DoesNotExist:
                continue
    
    # Calculate totals using Decimal arithmetic
    total = sum(
        item.total_price if hasattr(item, 'total_price') 
        else item.product.price * Decimal(item.quantity) 
        for item in cart_items
    )
    
    # Convert to Decimal for consistent arithmetic
    shipping = Decimal('5.99') if total > 0 else Decimal('0')
    tax = total * Decimal('0.08')  # 8% tax rate
    grand_total = total + shipping + tax
    
    return render(request, 'cart/view.html', {
        'cart_items': cart_items,
        'total': total,
        'shipping': shipping,
        'tax': tax,
        'grand_total': grand_total,
    })

@require_POST
@csrf_exempt
def add_to_cart(request):
    """Add item to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        
        if request.user.is_authenticated:
            # Authenticated user - use database cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # Anonymous user - use session cart
            cart = request.session.get('cart', {})
            cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
            request.session['cart'] = cart
            request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': f'{quantity} x {product.name} added to cart',
            'cart_count': get_cart_count(request)
        })
        
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid data format'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
@csrf_exempt
def update_cart(request):
    """Update cart item quantity via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        
        if quantity <= 0:
            return JsonResponse({'success': False, 'error': 'Quantity must be greater than 0'}, status=400)
        
        if request.user.is_authenticated:
            # Authenticated user - update database cart
            cart = Cart.objects.get(user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        else:
            # Anonymous user - update session cart
            cart = request.session.get('cart', {})
            cart[str(product_id)] = quantity
            request.session['cart'] = cart
            request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated successfully',
            'cart_count': get_cart_count(request)
        })
        
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid data format'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
@csrf_exempt
def remove_from_cart(request):
    """Remove item from cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        
        if request.user.is_authenticated:
            # Authenticated user - remove from database cart
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        else:
            # Anonymous user - remove from session cart
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart
                request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_count': get_cart_count(request)
        })
        
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid data format'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def get_cart_count(request):
    """Get the total number of items in cart"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            return 0
    else:
        cart = request.session.get('cart', {})
        return sum(cart.values())

@login_required
def checkout(request):
    """Checkout process"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('cart:view')
    
    total = sum(item.product.price * Decimal(item.quantity) for item in cart_items)
    
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def order_detail(request, order_id):
    """Order detail view"""
    # This would be implemented when Order model is properly set up
    return HttpResponse(f"<h1>Order {order_id}</h1><p>Order details.</p>")

@login_required
def orders(request):
    """Orders list view"""
    # This would be implemented when Order model is properly set up
    return HttpResponse("<h1>My Orders</h1><p>Your order history.</p>")