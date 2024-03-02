from django.urls import path 

from scheduler.views import index, display_all_users_timetables

urlpatterns = [
    path('', index, name='home'),
    path('tables/', display_all_users_timetables, name='tables'),
]