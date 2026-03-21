from rest_framework.serializers import ModelSerializer
from job_application.models import *

class MeetingSerializer(ModelSerializer):
  class Meta:
    model = Meeting
    exclude = ["employee"]