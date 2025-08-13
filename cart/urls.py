from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/', views.add_to_cart, name='add'),
    path('update/', views.update_cart, name='update'),
    path('remove/', views.remove_from_cart, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.orders, name='orders'),
    path('count/', views.get_cart_count, name='count'),
]