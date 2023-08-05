# Imports from Django.
from django.contrib import admin


class ElectionEventAdmin(admin.ModelAdmin):
    list_display = ("label", "get_date")
    ordering = ("election_day", "label")

    def get_date(self, obj):
        return obj.election_day.date

    get_date.short_description = "Date"
    get_date.admin_order_field = "election_day__date"
