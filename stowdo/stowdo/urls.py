from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from storage.urls import router as storage_router

router = routers.DefaultRouter()
router.registry.extend(storage_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('storage/', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls'))
]
