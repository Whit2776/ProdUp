from django.db import models

from app_1.models import Employment_Type, Role, Company, Employee


class Vacancy(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="vacancies",
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="vacancies")
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    application_fields = models.JSONField(
        blank=True,
        default=list,
        help_text=(
            "Dynamic application fields as JSON list. "
            "Example: [{'key': 'portfolio_url', 'label': 'Portfolio URL', 'type': 'url', 'required': False}]"
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.location})"

    def save(self, *args, **kwargs):
        if self.role_id and not self.company_id:
            self.company = self.role.company
        if self.role_id and self.company_id and self.role.company_id != self.company_id:
            raise ValueError("Vacancy.company must match Vacancy.role.company")
        return super().save(*args, **kwargs)


class Applicant(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applicants")
    employment_type = models.ForeignKey(Employment_Type, on_delete=models.PROTECT, related_name="applications")

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    resume = models.FileField(upload_to="applicant_uploads/resumes/")
    image = models.FileField(upload_to="applicant_uploads/images/")

    possible_start_date = models.DateField()
    extra_answers = models.JSONField(blank=True, default=dict)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["vacancy", "email"], name="unique_applicant_email_per_vacancy"),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.vacancy.title}"


class Meeting(models.Model):
  employee = models.ForeignKey(Employee, on_delete = models.PROTECT, related_name = 'meetings')
  applicant = models.ForeignKey(Applicant, on_delete = models.PROTECT, related_name = 'meetings')
  title = models.CharField(max_length = 300, null = True)
  scheduled_for = models.DateTimeField()
  created = models.DateTimeField(auto_now_add=True)
  event = models.OneToOneField("app_1.Event", on_delete=models.CASCADE)