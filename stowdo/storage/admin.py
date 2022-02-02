from django.contrib import admin
from storage.models import File, Folder

admin.register(Folder)
admin.register(File)