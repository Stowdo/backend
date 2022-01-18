from datetime import datetime
from rest_framework import serializers

from storage import models

# Folder serializers
class GetFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = ('pk', 'name', 'size', 'deleted', 'creation_date', 'user', 'parent_folder')


class CreateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = ('name', 'parent_folder')


class UpdateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = ('name', 'deleted', 'parent_folder')


# File serializers
class GetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('pk', 'name', 'size', 'deleted', 'upload_date', 'user', 'parent_folder')


class CreateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('path', 'parent_folder')


class UpdateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('name', 'deleted', 'parent_folder')