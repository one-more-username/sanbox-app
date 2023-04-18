from django.contrib import admin
from profiles.models import Profile


class AdminProfile(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Profile, AdminProfile)
