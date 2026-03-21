from django.urls import path

from . import views


urlpatterns = [
  path("/schedule-meeting", views.schedule_meeting)
]

