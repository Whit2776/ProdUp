from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.api.serializers import *
from app_1.models import *
from chat.models import *
from app_1.views import *

from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password, check_password

from datetime import datetime
from django.utils.timezone import make_aware
from decimal import Decimal, ROUND_HALF_UP

import secrets
import string
from django.shortcuts import get_object_or_404
from app_1.transaction import transfer
import time
from itertools import zip_longest

@api_view(['GET'])
def get_messages(request, link, num):
  employee = Employee.objects.get(emp_id=request.session.get('emp_id'))
  chat = Chat.objects.get(link = link)
  messages = chat.messages.all().order_by('-created')[0:num]

  received_messages = employee.received_messages.filter(chat = chat)
  print(received_messages)
  for m in received_messages:
    m.state = 'Read'
    m.save()

  serializer = MesSerializer(messages, many =True)
  data = serializer.data
  for d in data:
    files = list(File.objects.filter(message = Mes.objects.get(id = d['id'])))
    
    if len(files) > 0:
      files_json = [
        {
          "id": f.id,
          "path": f.path.url if f.path else None,
          "type": f.type,
          "name": f.name,
          "size": f.size,
        }
        for f in files
      ]
      d['files'] = files_json

  return Response(data)

@api_view(['GET'])
def get_message(request, link):
  if request.session.get('emp_id'):
    employee = Employee.objects.get(emp_id=request.session.get('emp_id'))
    chat = Chat.objects.get(link = link)
    messages = chat.messages.all()
    
    if not messages:
      return Response({'':''})
    
    def last(items):
      c = items.count()
      if c == 0:
        return 0
      return items[c-1]
    
    last_message = last(messages)
    files = list(File.objects.filter(message = last_message))
    dif = Decimal((make_aware(datetime.now()) - last_message.created).total_seconds()) if last_message != 0 else 0
    if dif <= 3:
      print(last_message.receiver)
      if employee == last_message.receiver and last_message.state == 'delivered':
        last_message.state = 'Read'
        last_message.save()
        print('😀 Gotten by Receiver')
      serializer = MesSerializer(last_message)
      data = serializer.data
      if len(files) > 0:
        files_json = [
          {
            "id": f.id,
            "path": f.path.url if f.path else None,
            "type": f.type,
            "name": f.name,
            "size": f.size,
          }
          for f in files
        ]
        data['files'] = files_json
      return Response(data)
    else:
      return Response({'':''})
  else:
    return Response({'':''})
  
@api_view(['POST'])
def post_message(request, link):
  r = request.data
  f = request.FILES
  employee = Employee.objects.get(emp_id=request.session.get('emp_id'))
  company = employee.company
  chat = Chat.objects.get(link = link)
  message = None
  ty = r.get('type')
  if ty == 'normal':
    message = Mes.objects.create(chat = chat, message = r.get('message'), sender=employee, receiver=chat.get_other_user(employee.id))
  elif ty == 'reply':
    message = Mes.objects.create(chat = chat, message = r.get('message'), sender=employee, receiver=chat.get_other_user(employee.id), type = ty, reply_to = r.get('reply_to_id'))
  elif ty == 'forward':
    ids = r.getlist('message-id')
    chats = r.getlist('chat')
    for id in ids:
      mes = Mes.objects.get(id = id)
      files = File.objects.filter(message = mes)
      for c in chats:
        chat = Chat.objects.get(link = c)
        message = Mes.objects.create(chat = chat, message = mes.message, sender = employee, receiver = chat.get_other_user(employee.id), type = ty)
        for g in files:
          file = File.objects.create(company = company, name=g.name, path = g.path, ext = g.ext, message = message, type=g.type)
    
  chat.order = message.created
  chat.save()

  for file in f.getlist('files'):
    name, ext = get_ext_name(file)
    fie = File.objects.create(company = company, name=name, path = file, ext = ext, message = message, type=get_type(file))

  
  message.state = 'delivered'
  message.save()

  serializer = MesSerializer(message)

  return Response(serializer.data)

@api_view(['POST'])
def delete_message(request):
  r = request.POST
  for id in r.getlist('ids'):
    mes = Mes.objects.get(id = id)
    mes.delete()
    
  return Response({'type':'alert', 'message': 'Successfully Deleted', 'success':True})