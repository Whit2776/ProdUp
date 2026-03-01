from django.shortcuts import render
from app_1.decorators import employee_login_required
from app_1.utils import render_dashboard
from .models import *
from app_1.models import *


@employee_login_required
def chatroom(request):
  employee = request.employee
  list = []
  chats = employee.chats.all().order_by('-order')
  for chat in chats:
    chat.other_user = chat.get_other_user(employee.id)
  context = {'chats':chats}
  return render_dashboard(request, 'chatroom.html', context)


@employee_login_required
def chat(request, link):
  employee = request.employee
  chat = Chat.objects.get(link = link)
  other_user = chat.get_other_user(employee.id)
  chat.other_user = other_user
  
  chats = employee.chats.all().order_by('-order')
  for c in chats:
    c.other_user = c.get_other_user(employee.id)
  context = {'chat':chat, 'chats':chats}
  return render_dashboard(request, 'chat_page.html', context)


@employee_login_required
def contact_list(request):
  context = {}
  return render_dashboard(request, 'contact-list.html', context)

# from uuid import uuid4

# employees = list(Employee.objects.all())

# for i in range(len(employees)):
#   for j in range(i + 1, len(employees)):  # avoid duplicates
#     e1 = employees[i]
#     e2 = employees[j]

#     # Check if a chat already exists between these 2
#     chat_exists = Chat.objects.filter(users=e1).filter(users=e2).exists()

#     if not chat_exists:
#       c = Chat.objects.create(
#           link=str(uuid4()),
#           type='chat'
#       )
#       c.users.set([e1, e2])
#       c.save()

#       print(f"Created chat: {e1.name} ↔ {e2.name}")