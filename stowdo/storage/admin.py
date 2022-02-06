from django.contrib import admin
from django.contrib.sites.models import Site
from storage.models import File, Folder
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp, EmailAddress


class FolderAdmin(admin.ModelAdmin):
    pass


class FileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)

admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)