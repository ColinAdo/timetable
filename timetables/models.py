from django.db import models
from django.conf import settings

class Timetable(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='timetables', 
        on_delete=models.CASCADE
        )
    batch_id = models.CharField(max_length=50, blank=True, null=True)
    day_of_week = models.CharField(max_length=200)
    lesson_time = models.CharField(max_length=200)
    unit_code = models.CharField(max_length=200)
    unit_name = models.CharField(max_length=200)
    lecturer = models.CharField(max_length=200, blank=True)
    campus = models.CharField(max_length=200, blank=True)
    mode_of_study = models.CharField(max_length=200, default='regular')
    room = models.CharField(max_length=200, blank=True)
    group = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.owner.username} timetable - {self.batch_id}"
