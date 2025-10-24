from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Home page view"""
    return render(request, 'core/home.html', {
        'title': 'Welcome to AgroMarket',
        'featured_products': [],
        'latest_posts': [],
    })

def about(request):
    """About page view"""
    return HttpResponse("<h1>About AgroMarket</h1><p>Agricultural marketplace connecting farmers worldwide.</p>")

def contact(request):
    """Contact page view"""
    return HttpResponse("<h1>Contact Us</h1><p>Get in touch with AgroMarket team.</p>")

def search(request):
    """Search functionality"""
    query = request.GET.get('q', '')
    return HttpResponse(f"<h1>Search Results</h1><p>You searched for: <strong>{query}</strong></p><p>Search functionality coming soon!</p>")