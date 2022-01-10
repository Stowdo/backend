from rest_framework import serializers

from storage import models


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = '__all__'