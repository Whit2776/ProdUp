from django.contrib import admin

from .models import Applicant, Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "role", "location", "salary_range", "is_active", "created_at")
    list_filter = ("is_active", "role__company")
    search_fields = ("title", "location", "role__position", "role__company__name")


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "vacancy", "employment_type", "submitted_at")
    list_filter = ("vacancy", "employment_type", "submitted_at")
    search_fields = ("name", "email", "phone", "vacancy__title")
