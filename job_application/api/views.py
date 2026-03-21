from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import MeetingSerializer

import datetime

@api_view(['POST'])
def schedule_meeting(request):
  employee = request.employee
  if not employee:
    return Response({"":""}, status = status.HTTP_403_FORBIDDEN)
  meeting_serializer = MeetingSerializer(data = request.data)
  if not meeting_serializer.is_valid():
    return Response({"message": "Invalid Data", "errors":meeting_serializer.errors}, status = status.HTTP_406_NOT_ACCEPTABLE)
  
  meeting = meeting_serializer.save(employee = employee)
  return Response({"success":True, "messsage":'Meeting successfully scheduled', "meeting_data":meeting_serializer.data})