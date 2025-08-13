from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Checkout and payment
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('buy-now/<int:product_id>/', views.BuyNowView.as_view(), name='buy_now'),
    path('process/<str:payment_id>/', views.PaymentProcessView.as_view(), name='process_payment'),
    
    # Webhooks
    path('webhook/<str:payment_id>/', views.payment_webhook, name='webhook'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
] 