from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from storage.urls import router as storage_router

urlpatterns = [
    path('', include(storage_router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('health/', include('health_check.urls')),
]