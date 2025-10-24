from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PaymentMethod, Order, OrderItem, Payment, 
    UserBalance, PaymentSecurity
)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'payment_type', 'is_active', 'processing_fee_percentage', 'processing_fee_fixed', 'min_amount', 'max_amount']
    list_filter = ['payment_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'payment_type', 'description', 'icon_class')
        }),
        ('Fees & Limits', {
            'fields': ('processing_fee_percentage', 'processing_fee_fixed', 'min_amount', 'max_amount')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'total_amount', 'grand_total', 'created_at', 'items_count']
    list_filter = ['status', 'created_at', 'customer']
    search_fields = ['order_number', 'customer__username', 'customer__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'status', 'created_at', 'updated_at')
        }),
        ('Financial', {
            'fields': ('total_amount', 'shipping_fee', 'tax_amount', 'grand_total')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address', 'notes')
        }),
    )
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer').prefetch_related('items')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'product__name']
    readonly_fields = ['total_price']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order_link', 'customer', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['payment_id', 'order__order_number', 'customer__username']
    readonly_fields = ['payment_id', 'created_at', 'updated_at', 'security_hash']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'order', 'customer', 'payment_method', 'status')
        }),
        ('Financial', {
            'fields': ('amount', 'processing_fee', 'total_amount')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'gateway_response')
        }),
        ('Security', {
            'fields': ('security_hash', 'ip_address', 'user_agent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:payments_order_change', args=[obj.order.id])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return '-'
    order_link.short_description = 'Order'
    order_link.admin_order_field = 'order__order_number'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'customer', 'payment_method')

@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'is_active', 'last_updated']
    list_filter = ['is_active', 'last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'is_active')
        }),
        ('Balance', {
            'fields': ('amount', 'last_updated')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(PaymentSecurity)
class PaymentSecurityAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'ip_address', 'risk_score', 'is_blocked', 'created_at']
    list_filter = ['event_type', 'is_blocked', 'created_at', 'risk_score']
    search_fields = ['ip_address', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('event_type', 'user', 'ip_address')
        }),
        ('Security Details', {
            'fields': ('user_agent', 'details', 'risk_score', 'is_blocked')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    actions = ['block_ip', 'unblock_ip']
    
    def block_ip(self, request, queryset):
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f'{updated} IP addresses have been blocked.')
    block_ip.short_description = "Block selected IP addresses"
    
    def unblock_ip(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f'{updated} IP addresses have been unblocked.')
    unblock_ip.short_description = "Unblock selected IP addresses"

# Customize admin site
admin.site.site_header = "AgroMarket Payment Administration"
admin.site.site_title = "AgroMarket Payments"
admin.site.index_title = "Payment System Management"
