from django.urls import path

from . import views


app_name = "job_application"

urlpatterns = [
    path(
        "job-applications/<uuid:company_uuid>/",
        views.company_vacancies,
        name="company_vacancies",
    ),
    path(
        "job-applications/<uuid:company_uuid>/vacancies/<int:pk>/",
        views.company_vacancy_detail,
        name="company_vacancy_detail",
    ),
    path(
        "job-applications/<uuid:company_uuid>/vacancies/<int:pk>/submitted/",
        views.company_application_submitted,
        name="company_application_submitted",
    ),
]

