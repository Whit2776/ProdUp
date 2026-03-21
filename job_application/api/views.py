from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view
def schedule_meeting(request):
  
  return Response({"messsage":'Meeting successfully scheduled'})