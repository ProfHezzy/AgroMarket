from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('category/<slug:slug>/', views.category_threads, name='category_threads'),
    path('thread/<slug:slug>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
    path('thread/<slug:slug>/reply/', views.add_post, name='add_post'),
]