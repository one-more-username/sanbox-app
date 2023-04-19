from django.contrib import admin

from .filters import FilterNoteWithSubnotes, FilterByCompletion
from .models import Note, SubNote


class SubNoteInline(admin.TabularInline):
    model = SubNote
    classes = ['collapse']


class AdminNote(admin.ModelAdmin):
    #   InlineModelAdmin
    inlines = [SubNoteInline]
    #
    list_display = ("id", "text", "is_done", 'time', 'priority')
    list_display_links = ("time", 'text')
    list_editable = ('is_done', 'priority')
    list_filter = ('is_done', FilterNoteWithSubnotes)
    # list_select_related = ('subnotes', )
    ordering = ('-priority',)
    search_fields = ['subnotes__text']
    # filter_vertical = ()  #   ?
    # filter_horizontal = ()    #   ?
    fieldsets = [
        ('Main options', {
            'fields': ("text", ('owner', 'priority'), "is_done", 'time')
        }),
        ('Advanced options', {
            'classes': ('collapse', 'extrapretty'),
            'fields': ('done_at', 'location'),
        }),
    ]
    actions = ['make_done', 'make_undone']

    @admin.action(description='Mark selected notes as doned')
    def make_done(self, request, queryset):
        queryset.update(is_done=True)

    @admin.action(description='Mark selected notes as undoned')
    def make_undone(self, request, queryset):
        queryset.update(is_done=False)


class AdminSubNote(admin.ModelAdmin):
    list_filter = ('is_done', FilterByCompletion)
    list_display = ("id", "estimated_time", "spent_time")


admin.site.register(SubNote, AdminSubNote)
admin.site.register(Note, AdminNote)
