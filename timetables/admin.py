from django.contrib import admin

from timetables.models import Timetable

class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        "owner", 
        "day_of_week", 
        "unit_code", 
        "unit_name", 
        "mode_of_study",
        "group"
    ]

admin.site.register(Timetable, TimetableAdmin)