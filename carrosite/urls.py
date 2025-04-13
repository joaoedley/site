from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('cars/', include('cars.urls')),
    path('custom-admin/', include('core.admin_urls')),  # Admin personalizado
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)