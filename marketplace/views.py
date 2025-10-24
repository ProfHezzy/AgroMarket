from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Product, Category

def product_list(request):
    """Product listing view"""
    # Get all products (temporarily removing is_active filter for debugging)
    products = Product.objects.all().order_by('-created_at')
    
    # Get all categories
    categories = Category.objects.all().order_by('name')
    
    # Apply filters if provided
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    # Apply search if provided
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Apply price filter if provided
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=float(price_min))
    if price_max:
        products = products.filter(price__lte=float(price_max))
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'price_min': price_min,
        'price_max': price_max,
    }
    
    return render(request, 'marketplace/index.html', context)

def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    # Get related products from the same category
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:4]
    
    return render(request, 'marketplace/detail.html', {
        'product': product,
        'related_products': related_products,
    })

def category_products(request, slug):
    """Category products view"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True).order_by('-created_at')
    
    return render(request, 'marketplace/category.html', {
        'category': category,
        'products': products,
    })

def search_products(request):
    """Search products view"""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(location__icontains=query),
            is_active=True
        ).order_by('-created_at')
    else:
        products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    categories = Category.objects.all().order_by('name')
    
    return render(request, 'marketplace/search.html', {
        'products': products,
        'query': query,
        'categories': categories,
    })

def add_product(request):
    """Add new product"""
    return HttpResponse("<h1>Add Product</h1><p>Product creation form.</p>")

def edit_product(request, pk):
    """Edit product"""
    return HttpResponse(f"<h1>Edit Product {pk}</h1><p>Product editing form.</p>")

def my_products(request):
    """My products view"""
    return HttpResponse("<h1>My Products</h1><p>Your product listings.</p>")

def wishlist(request):
    """Wishlist view"""
    return HttpResponse("<h1>My Wishlist</h1><p>Your saved products.</p>")