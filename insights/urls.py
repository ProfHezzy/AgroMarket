from django.urls import path
from . import views

app_name = 'insights'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/data/', views.api_data, name='api_data'),
    path('export/', views.export_data, name='export_data'),
]