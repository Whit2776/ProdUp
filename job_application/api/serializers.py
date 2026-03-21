from rest_framework.serializers import ModelSerializer
from job_application.models import *

class MeetingSerializer(ModelSerializer):
  model = Meeting
  fields = "__all__"