from rest_framework import routers

from storage import views

router = routers.DefaultRouter()
router.register('resources', views.ResourceViewSet, basename='resource')
router.register('folders', views.FolderViewSet, basename='folder')
router.register('files', views.FileViewSet, basename='file')

user_router = routers.DefaultRouter()
user_router.register('users', views.UserViewSet, basename='user')