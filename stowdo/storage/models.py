from django.contrib.auth import models as auth_models
from django.db import models
from django.dispatch import receiver


class Resource(models.Model):
    name = models.CharField(max_length=50)
    size = models.FloatField()
    deleted = models.BooleanField()
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)


class Folder(Resource):
    creation_date = models.DateTimeField()
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)


class File(Resource):
    path = models.FileField(default='')
    upload_date = models.DateTimeField()
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, default=None)


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.path:
        instance.path.delete(save=False)