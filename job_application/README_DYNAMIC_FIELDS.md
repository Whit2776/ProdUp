# Dynamic application fields

Vacancies can define extra application fields via `Vacancy.application_fields` (JSON).

The value should be a JSON list of objects, e.g.:

```json
[
  {
    "key": "portfolio_url",
    "label": "Portfolio URL",
    "type": "url",
    "required": false,
    "help_text": "Optional link to your work",
    "placeholder": "https://..."
  },
  {
    "key": "years_experience",
    "label": "Years of experience",
    "type": "number",
    "required": true
  },
  {
    "key": "stack",
    "label": "Primary stack",
    "type": "select",
    "required": true,
    "choices": ["Python", "JavaScript", "Java", "Other"]
  },
  {
    "key": "why_you",
    "label": "Why should we hire you?",
    "type": "textarea",
    "required": true
  }
]
```

Supported `type` values:

- `text` (default), `email`, `tel`, `url`, `number`, `date`, `textarea`
- `select`, `radio` (use `choices`)
- `checkbox`

On submission, these values are stored in `Applicant.extra_answers` using the same `key` values.

