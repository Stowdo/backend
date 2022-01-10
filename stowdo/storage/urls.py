from rest_framework import routers

from storage import views

router = routers.DefaultRouter()
router.register('folders', views.FolderViewSet)
router.register('files', views.FileViewSet)