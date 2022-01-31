from datetime import datetime
from django import http
from rest_framework import viewsets, permissions, decorators, exceptions

from storage import models, serializers


def check_parent_folder(request):
    if request.data.get('parent_folder', '').isdigit():
        folder_id = request.data['parent_folder']
        folder_query = models.Folder.objects.filter(pk=folder_id, user=request.user)

        if not folder_query.exists():
            raise exceptions.PermissionDenied()


class FolderViewSet(viewsets.ModelViewSet):
    queryset = models.Folder.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('user', 'parent_folder', 'deleted')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.GetFolderSerializer
        elif self.action == 'create':
            return serializers.CreateFolderSerializer
        return serializers.UpdateFolderSerializer

    def get_queryset(self):
        return models.Folder.objects.filter(user=self.request.user)

    # creation
    def create(self, request):
        check_parent_folder(request)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(size=0, deleted=False, user=self.request.user, creation_date=datetime.now())
    
    # read
    def retrieve(self, request, pk):
        if models.Folder.objects.filter(pk=pk, user=request.user).exists():
            return super().retrieve(request, pk)
        raise exceptions.PermissionDenied()

    # update
    def update(self, request, pk):
        check_parent_folder(request)
        return super().update(request, pk)


class FileViewSet(viewsets.ModelViewSet):
    queryset = models.File.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('user', 'parent_folder', 'deleted')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.GetFileSerializer
        elif self.action == 'create':
            return serializers.CreateFileSerializer
        return serializers.UpdateFileSerializer

    @decorators.action(detail=True)
    def download(self, request, pk):
        file = self.get_object()
        if file.user == self.request.user:
            try:
                reader = file.path.open()
            except Exception:
                pass
            else:
                response = http.FileResponse(reader)
                response['Content-Length'] = file.path.size
                response['Content-Disposition'] = f'attachment; filename="{file.name}"'

                return response
        else:
            return http.Http404()

    def get_queryset(self):
        return models.File.objects.filter(user=self.request.user)

    # create
    def create(self, request):
        check_parent_folder(request)
        response = super().create(request)

        if request.data.get('parent_folder', None):
            folder = models.Folder.objects.get(pk=request.data['parent_folder'])
            folder.size += request.data['path'].size
        return response

    def perform_create(self, serializer):
        if hasattr(self.request, 'data'):
            file = getattr(self.request, 'data').get('path')
        else:
            file = list(self.request.FILES['path'])[0]

        serializer.save(
            name=file.name,
            size=file.size,
            deleted=False,
            user=self.request.user,
            path=file,
            upload_date=datetime.now())
    
    def retrieve(self, request, pk):
        if models.File.objects.filter(pk=pk, user=request.user).exists():
            return super().retrieve(request, pk)
        raise exceptions.PermissionDenied()

    def update(self, request, pk):
        request.data['upload_date'] = datetime.now()
        check_parent_folder(request)
        return super().update(request, pk)

    def partial_update(self, request, pk):
        check_parent_folder(request)
        return super().partial_update(request, pk)