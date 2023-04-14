from django.contrib import admin

from .models import Note, SubNote

admin.site.register(SubNote)


class AdminNote(admin.ModelAdmin):
    list_display = ("id", "text", "is_done")


admin.site.register(Note, AdminNote)
