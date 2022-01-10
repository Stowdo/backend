from django.contrib.auth import models as auth_models
from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=50)
    size = models.FloatField()
    deleted = models.BooleanField()
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)


class Folder(Resource):
    creation_date = models.DateTimeField()
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE)


class File(Resource):
    path = models.CharField(max_length=256)
    update_date = models.DateTimeField()
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)