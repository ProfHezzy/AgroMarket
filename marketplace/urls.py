from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('search/', views.search_products, name='search_products'),
    path('add/', views.add_product, name='add_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('my-products/', views.my_products, name='my_products'),
    path('wishlist/', views.wishlist, name='wishlist'),
]