from django.contrib import admin

from .models import *


admin.site.register(Vacancy)
admin.site.register(Applicant)
admin.site.register(Meeting)
admin.site.register(MeetingParticipant)