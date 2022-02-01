from django.contrib.auth.models import User
from rest_framework import serializers

from storage.models import File, Folder, Resource

class EmptySerializer(serializers.Serializer):
    pass


# User serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SimplifiedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


# Resource serializers
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource


class DownloadResourcesSerializer(serializers.Serializer):
    folders = serializers.PrimaryKeyRelatedField(many=True, queryset=Folder.objects.all())
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all())


# Folder serializers
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class CreateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'parent_folder')


class UpdateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'deleted', 'parent_folder')


class DownloadFoldersSerializer(serializers.Serializer):
    folders = serializers.PrimaryKeyRelatedField(many=True, queryset=Folder.objects.all())


# File serializers
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CreateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('path', 'parent_folder')


class UpdateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'deleted', 'parent_folder')


class DownloadFilesSerializer(serializers.Serializer):
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all())