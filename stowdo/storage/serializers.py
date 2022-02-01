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
        fields = ['name', 'parent_folder']
    
    def save(self, **kwargs):
        self.Meta.fields = ['pk', 'name', 'size', 'deleted', 'creation_date', 'user', 'parent_folder']
        return super().save(**kwargs)


class UpdateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = ['name', 'deleted', 'parent_folder']

    def save(self, **kwargs):
        self.Meta.fields = ['pk', 'name', 'size', 'deleted', 'creation_date', 'user', 'parent_folder']
        return super().save(**kwargs)


class DownloadFoldersSerializer(serializers.Serializer):
    folders = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Folder.objects.all())


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


class DownloadFilesSerializer(serializers.Serializer):
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=models.File.objects.all())