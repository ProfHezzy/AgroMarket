"""
URL configuration for AgroMarket project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('forum/', include('forum.urls')),
    path('cart/', include('cart.urls')),
    path('insights/', include('insights.urls')),
    path('payments/', include('payments.urls')),
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers will be added later
# handler404 = 'core.views.handler404'
# handler500 = 'core.views.handler500'