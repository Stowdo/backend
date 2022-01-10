from rest_framework import viewsets, permissions

from storage import models, serializers


class FolderViewSet(viewsets.ModelViewSet):
    queryset = models.Folder.objects.all()
    serializer_class = serializers.FolderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('user', 'parent_folder', 'deleted')


class FileViewSet(viewsets.ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('user', 'parent_folder', 'deleted')