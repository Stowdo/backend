from datetime import datetime
from django.http import HttpResponseBadRequest
from rest_framework import permissions, decorators
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from storage.models import Folder, File, Resource
from storage.serializers import CreateFolderSerializer, DownloadFilesSerializer, DownloadFoldersSerializer, GetFolderSerializer, UpdateFolderSerializer, \
    CreateFileSerializer, GetFileSerializer, UpdateFileSerializer
from storage.utils import create_file_response, create_zip_response, check_parent_folder


class ResourceViewSet(ModelViewSet):
    http_method_names = ['post', 'head', 'options', 'trace']
    queryset = Resource.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    @decorators.action(detail=False, methods=['post'])
    def download(self, request):
        user = request.user
        folders_pk = request.data.get('folders', [])
        files_pk = request.data.get('files', [])

        if isinstance(folders_pk, list) and isinstance(files_pk, list):
            return create_zip_response(user, folders_pk, files_pk)
        return HttpResponseBadRequest('"folders" and "files" must be json arrays')


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'download'):
            return GetFolderSerializer
        elif self.action == 'create':
            return CreateFolderSerializer
        elif self.action == 'download_multiple':
            return DownloadFoldersSerializer
        return UpdateFolderSerializer

    def get_queryset(self):
        if hasattr(self.request, 'query_params'):
            parent_folder = getattr(self.request, 'query_params').get('parent_folder', None)
        else:
            parent_folder = None

        if parent_folder == None:
            return Folder.objects.filter(user=self.request.user)
        elif parent_folder == '':
            return Folder.objects.filter(user=self.request.user, parent_folder__isnull=True)
        return Folder.objects.filter(user=self.request.user, parent_folder=parent_folder)

    # creation
    def create(self, request):
        check_parent_folder(request)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(size=0, deleted=False, user=self.request.user, creation_date=datetime.now())
    
    # read
    def retrieve(self, request, pk):
        if Folder.objects.filter(pk=pk, user=request.user).exists():
            return super().retrieve(request, pk)
        raise PermissionDenied()

    # update
    def update(self, request, pk):
        check_parent_folder(request)
        return super().update(request, pk)
    
    # delete
    def destroy(self, request, pk=None):
        if Folder.objects.filter(pk=pk, user=request.user).exists():
            return super().destroy(request, pk)
        raise PermissionDenied()

    # special actions
    @decorators.action(detail=True)
    def download(self, request, pk):
        return create_zip_response(request.user, [pk], [])

    @decorators.action(detail=False, methods=['post'], url_name='download')
    def download_multiple(self, request):
        folders_pk = request.data.get('folders', [])

        if isinstance(folders_pk, list):
            return create_zip_response(request.user, folders_pk, [])
        return HttpResponseBadRequest('"folders" must be a json array')


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'download'):
            return GetFileSerializer
        elif self.action == 'create':
            return CreateFileSerializer
        elif self.action == 'download_multiple':
            return DownloadFilesSerializer
        return UpdateFileSerializer

    def get_queryset(self):
        if hasattr(self.request, 'query_params'):
            parent_folder = getattr(self.request, 'query_params').get('parent_folder', None)
        else:
            parent_folder = None

        if parent_folder == None:
            return File.objects.filter(user=self.request.user)
        elif parent_folder == '':
            return File.objects.filter(user=self.request.user, parent_folder__isnull=True)
        return File.objects.filter(user=self.request.user, parent_folder=parent_folder)

    # create
    def create(self, request):
        check_parent_folder(request)
        response = super().create(request)

        if request.data.get('parent_folder', None):
            folder = Folder.objects.get(pk=request.data['parent_folder'])
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
    
    # read
    def retrieve(self, request, pk):
        if File.objects.filter(pk=pk, user=request.user).exists():
            return super().retrieve(request, pk)
        raise PermissionDenied()

    # update
    def update(self, request, pk):
        check_parent_folder(request)
        return super().update(request, pk)

    def partial_update(self, request, pk):
        check_parent_folder(request)
        return super().partial_update(request, pk)

    def perform_update(self, serializer):
        serializer.save(upload_date=datetime.now())

    # delete
    def destroy(self, request, pk=None):
        if File.objects.filter(pk=pk, user=request.user).exists():
            return super().destroy(request, pk)
        raise PermissionDenied()

    # special actions
    @decorators.action(detail=True)
    def download(self, request, pk):
        return create_file_response(request.user, pk)

    @decorators.action(detail=False, methods=['post'], url_path='download')
    def download_multiple(self, request):
        files_pk = request.data.get('files', [])

        if isinstance(files_pk, list):
            return create_zip_response(request.user, [], files_pk)
        return HttpResponseBadRequest('"files" must be a json array')