from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicantForm
from .models import Vacancy


def vacancy_list(request):
    vacancies = (
        Vacancy.objects.filter(is_active=True)
        .select_related("role", "role__company")
        .order_by("-created_at")
    )
    return render(request, "job_application/vacancy_list.html", {"vacancies": vacancies})


def vacancy_detail(request, pk: int):
    vacancy = get_object_or_404(
        Vacancy.objects.select_related("role", "role__company").filter(is_active=True),
        pk=pk,
    )

    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES, vacancy=vacancy)
        if form.is_valid():
            form.save()
            return redirect("job_application:application_submitted", pk=vacancy.pk)
    else:
        form = ApplicantForm(vacancy=vacancy)

    return render(
        request,
        "job_application/vacancy_detail.html",
        {
            "vacancy": vacancy,
            "form": form,
        },
    )


def application_submitted(request, pk: int):
    vacancy = Vacancy.objects.filter(pk=pk).first()
    if not vacancy:
        raise Http404
    return render(request, "job_application/application_success.html", {"vacancy": vacancy})
