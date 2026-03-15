from django.urls import path

from . import views


app_name = "job_application"

urlpatterns = [
    path("", views.vacancy_list, name="vacancy_list"),
    path("vacancies/<int:pk>/", views.vacancy_detail, name="vacancy_detail"),
    path("vacancies/<int:pk>/submitted/", views.application_submitted, name="application_submitted"),
]

