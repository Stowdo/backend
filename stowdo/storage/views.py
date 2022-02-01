from datetime import datetime
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import permissions, decorators
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from storage.models import Folder, File, Resource
from storage.serializers import \
    UserSerializer, SimplifiedUserSerializer, \
    FolderSerializer, CreateFolderSerializer, UpdateFolderSerializer, DownloadFoldersSerializer, \
    FileSerializer, CreateFileSerializer, UpdateFileSerializer, DownloadFilesSerializer, \
    ResourceSerializer, DownloadResourcesSerializer, EmptySerializer
from storage.utils import create_file_response, create_zip_response, check_parent_folder


class UserViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        if getattr(self.request.user, 'is_staff', False):
            return UserSerializer
        return SimplifiedUserSerializer

    def get_queryset(self):
        if getattr(self.request.user, 'is_staff', False):
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    def list(self, request):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().list(request)

    def create(self, request):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().create(request)

    def retrieve(self, request, pk):
        if str(pk).isdigit():
            if request.user.pk == int(pk) or request.user.is_staff:
                return super().retrieve(request, pk)
        raise PermissionDenied()

    def update(self, request, pk):
        if str(pk).isdigit():
            if request.user.pk == int(pk) or request.user.is_staff:
                return super().update(request, pk)
        raise PermissionDenied()

    def destroy(self, request, pk):
        if str(pk).isdigit():
            if request.user.pk == int(pk) or request.user.is_staff:
                return super().destroy(request, pk)
        raise PermissionDenied()


class ResourceViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'download_multiple':
            return DownloadResourcesSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return EmptySerializer
        return ResourceSerializer

    def get_queryset(self):
        if getattr(self.request.user, 'is_staff', False):
            return Resource.objects.all()
        return Resource.objects.filter(user=self.request.user)

    def list(self, request):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().list(request)

    def create(self, _):
        return PermissionDenied()

    def retrieve(self, request, pk):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().retrieve(request, pk)

    def update(self, _):
        return PermissionDenied()

    @decorators.action(detail=False, methods=['post'], url_name='download')
    def download_multiple(self, request):
        user = request.user
        folders_pk = request.data.get('folders', [])
        files_pk = request.data.get('files', [])

        if isinstance(folders_pk, list) and isinstance(files_pk, list):
            return create_zip_response(user, folders_pk, files_pk)
        return HttpResponseBadRequest('"folders" and "files" must be json arrays')


class FolderViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        filters = {}
        query_params = getattr(self.request, 'query_params', {})
        parent_folder = query_params.get('parent_folder', None)

        if parent_folder == '':
            filters['parent_folder'] = None
        elif parent_folder != None:
            filters['parent_folder'] = parent_folder
        if not getattr(self.request.user, 'is_staff', False):
            filters['user'] = self.request.user

        return Folder.objects.filter(**filters)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFolderSerializer
        if self.action == 'download_multiple':
            return DownloadFoldersSerializer
        if getattr(self.request.user, 'is_staff', False) \
            and self.action in ('update', 'partial_update'):
            return UpdateFolderSerializer
        return FolderSerializer

    def create(self, request):
        if not request.user.is_staff:
            check_parent_folder(request)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(size=0, deleted=False, user=self.request.user, creation_date=datetime.now())

    def retrieve(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        if request.user.is_staff:
            if folder.user != request.user:
                raise PermissionDenied('You do not have the permission to retrieve this folder')

        return super().retrieve(request, pk)

    def update(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        if request.user.is_staff:
            check_parent_folder(request)

            if folder.user != request.user:
                raise PermissionDenied('You do not have the permission to update this folder')

        return super().update(request, pk)
    
    def destroy(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        if request.user.is_staff:
            if folder.user != request.user:
                raise PermissionDenied('You do not have the permission to destroy this folder')

        return super().destroy(request, pk)

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
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        filters = {}
        query_params = getattr(self.request, 'query_params', {})
        parent_folder = query_params.get('parent_folder', None)

        if parent_folder == '':
            filters['parent_folder'] = None
        elif parent_folder != None:
            filters['parent_folder'] = parent_folder
        if not getattr(self.request.user, 'is_staff', False):
            filters['user'] = self.request.user
            
        return File.objects.filter(**filters)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFileSerializer
        if self.action == 'download_multiple':
            return DownloadFilesSerializer
        if getattr(self.request.user, 'is_staff', False) \
            and self.action in ('update', 'partial_update'):
            return UpdateFileSerializer
        return FileSerializer

    def create(self, request):
        if not request.user.is_staff:
            check_parent_folder(request)
        
        parent_folder_id = request.data.get('parent_folder', None)
        if str(parent_folder_id).isdigit():
            parent_folder = get_object_or_404(Folder, pk=int(parent_folder_id))
            file_size = request.data.get('path', DjangoFile).size

            while parent_folder:
                parent_folder.size += file_size
                parent_folder.save()
                parent_folder = parent_folder.parent_folder
        
        return super().create(request)

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
            upload_date=datetime.now()
        )

    def retrieve(self, request, pk):
        file = get_object_or_404(File, pk=pk)
        if request.user.is_staff:
            if file.user != request.user:
                raise PermissionDenied('You do not have the permission to retrieve this file')

        return super().retrieve(request, pk)

    def update(self, request, pk):
        file = get_object_or_404(File, pk=pk)
        if request.user.is_staff:
            check_parent_folder(request)

            if file.user != request.user:
                raise PermissionDenied('You do not have the permission to update this file')

        return super().update(request, pk)

    def perform_update(self, serializer):
        serializer.save(upload_date=datetime.now())

    def destroy(self, request, pk=None):
        file = get_object_or_404(File, pk=pk)
        if request.user.is_staff:
            if file.user != request.user:
                raise PermissionDenied('You do not have the permission to destroy this file')
        
        parent_folder = file.parent_folder
        while parent_folder:
            parent_folder.size -= file.size
            parent_folder.save()
            parent_folder = parent_folder.parent_folder

        return super().destroy(request, pk)

    @decorators.action(detail=True)
    def download(self, request, pk):
        return create_file_response(request.user, pk)

    @decorators.action(detail=False, methods=['post'], url_path='download')
    def download_multiple(self, request):
        files_pk = request.data.get('files', [])

        if isinstance(files_pk, list):
            return create_zip_response(request.user, [], files_pk)
        return HttpResponseBadRequest('"files" must be a json array')