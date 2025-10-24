from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def dashboard(request):
    """Analytics dashboard"""
    return render(request, 'insights/index.html', {
        'total_products': 150,
        'active_sellers': 25,
        'avg_price': 45.99,
        'total_orders': 320,
        'categories': [],
        'top_products': [],
        'top_categories': [],
        'detailed_products': [],
    })

def api_data(request):
    """API endpoint for dashboard data"""
    return JsonResponse({
        'price_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'price_data': [25, 30, 28, 35, 32],
        'sales_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'sales_data': [10, 15, 12, 20, 18],
        'category_labels': ['Fruits', 'Vegetables', 'Grains'],
        'category_data': [40, 35, 25],
    })

def export_data(request):
    """Export dashboard data"""
    format_type = request.GET.get('format', 'csv')
    return HttpResponse(f"<h1>Export Data</h1><p>Exporting data as {format_type}.</p>")