from django.contrib import admin

from .models import Note, SubNote


class FilterByGoodTime(admin.SimpleListFilter):
    title = 'good time'
    parameter_name = 'good_time'

    def lookups(self, request, model_admin):
        return [('good_time', 'good time'), ]

    def queryset(self, request, queryset):
        if self.value() == 'good_time':
            for qs_item in queryset.values():
                if qs_item['spent_time']:
                    qs = queryset.filter(
                        estimated_time__lte=qs_item['spent_time'],
                        spent_time__isnull=False
                    )
            return qs


class FilterByBadTime(admin.SimpleListFilter):
    title = 'bad time'
    parameter_name = 'bad_time'

    def lookups(self, request, model_admin):
        return [('bad_time', 'bad time'), ]

    def queryset(self, request, queryset):
        if self.value() == 'bad_time':
            for qs_item in queryset.values():
                if qs_item['spent_time']:
                    qs = queryset.filter(
                        estimated_time__gt=qs_item['spent_time'],
                        spent_time__isnull=False
                    )
            return qs


class SubNoteInline(admin.TabularInline):
    model = SubNote
    classes = ['collapse']


class AdminSubNote(admin.ModelAdmin):
    list_filter = ('is_done', FilterByGoodTime, FilterByBadTime)


class AdminNote(admin.ModelAdmin):
    #   InlineModelAdmin
    inlines = [SubNoteInline]
    #
    list_display = ("id", "text", "is_done", 'time', 'priority')
    list_display_links = ("time", 'text')
    list_editable = ('is_done', 'priority')
    list_filter = ('is_done', )
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


admin.site.register(SubNote, AdminSubNote)
admin.site.register(Note, AdminNote)
