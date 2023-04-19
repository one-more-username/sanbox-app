from django.contrib import admin
from django.db.models import F


class FilterNoteWithSubnotes(admin.SimpleListFilter):
    title = 'subnotes'
    parameter_name = 'subnotes'

    def lookups(self, request, model_admin):
        return [('subnotes', 'With subnotes'), ]

    def queryset(self, request, queryset):
        if self.value() == 'subnotes':
            return queryset.filter(subnotes__isnull=False, ).distinct()


class FilterByCompletion(admin.SimpleListFilter):
    title = 'completion'
    parameter_name = 'completion'

    def lookups(self, request, model_admin):
        return [
            ('completed_on_time', 'Completed on time'),
            ('not_completed_on_time', 'Not completed on time')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'completed_on_time':
            return queryset.filter(
                spent_time__isnull=False,
                estimated_time__gte=F('spent_time'))
        elif self.value() == 'not_completed_on_time':
            return queryset.filter(
                spent_time__isnull=False,
                estimated_time__lt=F('spent_time'))
        else:
            return queryset
