from django.urls import path

from . import views


urlpatterns = [
  path("schedule-meeting", views.schedule_meeting),
  path("applicant-meeting-exists/<int:id>", views.applicant_meeting_exists),
]

