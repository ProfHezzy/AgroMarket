from django.contrib import admin
from .models import PriceHistory, MarketTrend

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['product__name']
    readonly_fields = ['recorded_at']

@admin.register(MarketTrend)
class MarketTrendAdmin(admin.ModelAdmin):
    list_display = ['category', 'average_price', 'total_sales', 'date', 'created_at']
    list_filter = ['category', 'date', 'created_at']
    readonly_fields = ['created_at']