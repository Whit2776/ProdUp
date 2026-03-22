from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from app_1.models import Employee, Client
from app_1.brevo import send_brevo_email

from job_application.models import Meeting, MeetingParticipant, Applicant

from .serializers import MeetingSerializer

import datetime

@api_view(['POST'])
def schedule_meeting(request):
  company = request.company
  employee = request.employee
  
  if not (company and employee):
    return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
  
  r = request.data
  MODEL_MAP = {
    "employee": Employee,
    "applicant": Applicant,
    "client": Client,
  }
  
  sent = 0
  failed = 0
  total_participants = 0
  meeting_serializer = MeetingSerializer(data = request.data)
  
  if not meeting_serializer.is_valid():
    return Response({"message": "Invalid Data", "errors":meeting_serializer.errors}, status = status.HTTP_406_NOT_ACCEPTABLE)
  meeting = meeting_serializer.save(created_by = employee)
  participants = [MeetingParticipant(meeting = meeting, object_id = employee.id, content_type = ContentType.objects.get_for_model(Employee), role = 'host')]
  
  for p in r.getlist('participants'):
    total_participants += 1
    with transaction.atomic():
      id, content_type, email, name = p.split('_')
      participants.append(
        MeetingParticipant(
          meeting = meeting,
          object_id = id,
          content_type = ContentType.objects.get_for_model(MODEL_MAP.get(content_type)),
        )
      )
      status_code, text = send_brevo_email(8, email, name, {"subject":"Meeting Scheduled", "content": f"You have been selected for a meeting on {meeting.scheduled_for.date()} at {meeting.scheduled_for.time()}" , "company_name":company.name})
      if status_code == 201:
        sent += 1
      else:
        print("Error: ", text)
        failed += 1
    meeting_participants = MeetingParticipant.objects.bulk_create(participants)
  return Response({"success":True, "messsage":'Meeting successfully scheduled', "meeting_data":meeting_serializer.data, "email_success": f"{sent} emails sent to {total_participants} participants. {failed} failed"})

@api_view(['GET'])
def applicant_meeting_exists(reqeust, id):
  company = reqeust.company
  if not company:
    return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
  
  meeting_applicant = MeetingParticipant.objects.filter(content_type = ContentType.objects.get_for_model(Applicant), object_id = id).first()
  if not meeting_applicant:
    return Response({"success": False}, status = status.HTTP_404_NOT_FOUND)
  meeting = MeetingSerializer(meeting_applicant.meeting).data
  
  if meeting_applicant:
    return Response({"success": True, "meeting":meeting})
  return Response({"success":False})