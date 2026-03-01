import requests
from django.conf import settings

def send_brevo_email(template_id, to_email, to_name, params):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": settings.BREVO_API_KEY,
    }
    
    sender = {
      "email": settings.DEFAULT_FROM_EMAIL,
      "name": "Family App"
    }

    data = {
        "templateId": template_id,
        "to": [
            {
                "email": to_email,
                "name": to_name
            }
        ],
        "params": params
    }

    response = requests.post(url, json=data, headers=headers)
    
    print(response.status_code)
    print('BODY, ', response.text)
    return response.status_code, response.text
