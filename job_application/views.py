from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app_1.models import Company

from .forms import ApplicantForm
from .models import Vacancy


def vacancy_list(request):
    raise Http404


def vacancy_detail(request, pk: int):
    raise Http404


def application_submitted(request, pk: int):
    raise Http404


def company_vacancies(request, company_uuid):
    company = get_object_or_404(Company, company_uuid=company_uuid)
    vacancies = (
        Vacancy.objects.filter(company=company, is_active=True)
        .select_related("role")
        .order_by("-created_at")
    )
    return render(
        request,
        "job_application/company_vacancies.html",
        {"company": company, "vacancies": vacancies},
    )


def company_vacancy_detail(request, company_uuid, pk: int):
    company = get_object_or_404(Company, company_uuid=company_uuid)
    vacancy = get_object_or_404(
        Vacancy.objects.select_related("role").filter(company=company, is_active=True),
        pk=pk,
    )

    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES, vacancy=vacancy)
        if form.is_valid():
            form.save()
            return redirect(
                "job_application:company_application_submitted",
                company_uuid=company_uuid,
                pk=vacancy.pk,
            )
    else:
        form = ApplicantForm(vacancy=vacancy)

    return render(
        request,
        "job_application/vacancy_detail.html",
        {
            "company": company,
            "vacancy": vacancy,
            "form": form,
        },
    )


def company_application_submitted(request, company_uuid, pk: int):
    company = get_object_or_404(Company, company_uuid=company_uuid)
    vacancy = get_object_or_404(Vacancy.objects.filter(company=company), pk=pk)
    return render(
        request,
        "job_application/application_success.html",
        {"company": company, "vacancy": vacancy},
    )
