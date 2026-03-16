from __future__ import annotations

from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from app_1.models import Employment_Type

from .models import Applicant, Vacancy


def _validate_ext(file_obj, allowed_exts: set[str], field_label: str) -> None:
    name = getattr(file_obj, "name", "")
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in allowed_exts:
        raise ValidationError(f"{field_label} must be one of: {', '.join(sorted(allowed_exts))}.")


class ApplicantForm(forms.ModelForm):
    """
    Dynamic applicant form:
    - Base fields come from Applicant model.
    - Extra fields are described by Vacancy.application_fields JSON.
    - Extra values are persisted into Applicant.extra_answers.
    """

    class Meta:
        model = Applicant
        fields = [
            "name",
            "email",
            "phone",
            "employment_type",
            "possible_start_date",
            "resume",
            "image",
        ]
        widgets = {
            "possible_start_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args: Any, vacancy: Vacancy, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.vacancy = vacancy

        company = getattr(vacancy, "company", None) or getattr(vacancy.role, "company", None)
        if company is not None:
            self.fields["employment_type"].queryset = Employment_Type.objects.filter(company=company).order_by("type")

        # Build dynamic fields from vacancy.application_fields
        self._dynamic_keys: list[str] = []
        field_specs = vacancy.application_fields or []
        if not isinstance(field_specs, list):
            field_specs = []

        for spec in field_specs:
            if not isinstance(spec, dict):
                continue

            key = str(spec.get("key", "")).strip()
            if not key:
                continue

            label = str(spec.get("label", key)).strip() or key
            required = bool(spec.get("required", False))
            help_text = str(spec.get("help_text", "")).strip()
            placeholder = str(spec.get("placeholder", "")).strip()

            field_type = str(spec.get("type", "text")).strip().lower()
            choices = spec.get("choices", None)

            if field_type in {"select", "radio"} and isinstance(choices, list) and choices:
                normalized = []
                for c in choices:
                    if isinstance(c, (list, tuple)) and len(c) == 2:
                        normalized.append((str(c[0]), str(c[1])))
                    else:
                        normalized.append((str(c), str(c)))
                field_cls = forms.ChoiceField
                widget = forms.Select if field_type == "select" else forms.RadioSelect
                field = field_cls(
                    choices=normalized,
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=widget(),
                )
            elif field_type == "textarea":
                field = forms.CharField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.Textarea(attrs={"rows": 4, "placeholder": placeholder}),
                )
            elif field_type == "email":
                field = forms.EmailField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.EmailInput(attrs={"placeholder": placeholder}),
                )
            elif field_type == "tel":
                field = forms.CharField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.TextInput(attrs={"inputmode": "tel", "placeholder": placeholder}),
                )
            elif field_type == "url":
                field = forms.URLField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.URLInput(attrs={"placeholder": placeholder}),
                )
            elif field_type == "number":
                field = forms.DecimalField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.NumberInput(attrs={"placeholder": placeholder}),
                )
            elif field_type == "date":
                field = forms.DateField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.DateInput(attrs={"type": "date"}),
                )
            elif field_type == "checkbox":
                field = forms.BooleanField(
                    required=required,
                    label=label,
                    help_text=help_text,
                )
            else:
                field = forms.CharField(
                    required=required,
                    label=label,
                    help_text=help_text,
                    widget=forms.TextInput(attrs={"placeholder": placeholder}),
                )

            self.fields[key] = field
            self._dynamic_keys.append(key)

        # UX tweaks
        self.fields["resume"].help_text = "PDF only."
        self.fields["image"].help_text = "JPEG/PNG/MP4."

    def clean_resume(self):
        f = self.cleaned_data.get("resume")
        if not f:
            return f
        _validate_ext(f, {"pdf"}, "Resume/CV")
        return f

    def clean_image(self):
        f = self.cleaned_data.get("image")
        if not f:
            return f
        _validate_ext(f, {"jpg", "jpeg", "png", "mp4"}, "Image")
        return f

    def clean(self):
        cleaned = super().clean()
        # Enforce unique email per vacancy at the form level for nicer errors.
        email = cleaned.get("email")
        if email and Applicant.objects.filter(vacancy=self.vacancy, email=email).exists():
            self.add_error("email", "This email has already applied for this vacancy.")
        return cleaned

    def save(self, commit: bool = True) -> Applicant:
        instance: Applicant = super().save(commit=False)
        instance.vacancy = self.vacancy

        extra: dict[str, Any] = {}
        for key in getattr(self, "_dynamic_keys", []):
            # Store even False for checkbox if present in form; omit if not provided.
            if key in self.cleaned_data:
                extra[key] = self.cleaned_data.get(key)
        instance.extra_answers = extra

        if commit:
            instance.save()
            self.save_m2m()
        return instance

