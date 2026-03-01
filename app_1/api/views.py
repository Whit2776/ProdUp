from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app_1.api.serializers import *
from app_1.models import *
from chat.models import *
from app_1.views import *
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password, check_password
from django.http import *
from django.urls import reverse
import os
import uuid
from datetime import datetime
from django.utils.timezone import make_aware
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.shortcuts import get_object_or_404

from django.db import transaction

from app_1.transaction import transfer
from app_1.brevo import send_brevo_email


@api_view(["POST"])
def post_message(request):
  r = request.POST
  rf=request.FILES
  

  
  name = r.get('name')
  phone_number = r.get('phone_number')
  email = r.get('email')
  subject = r.get('subject')
  msg = r.get('msg')

  
  user = User.objects.update_or_create(name = name, phone_number = phone_number, email = email)

  request.session['user_id'] = user.id


  body = f"""
    Hello {name}, we have recieved your email and we will contact you through your;
    Email: {email}

    or

    Phone: {phone_number}

    Cheers
    """

  mail = EmailMessage(
      subject=subject,
      body=body,
      from_email=settings.DEFAULT_FROM_EMAIL,
      to=[email],
      reply_to=[email],
    )
  
  company = Company.objects.get(id = 1)

  message = Message.objects.create(
    company = company,
    name = name, 
    email = email, 
    subject=subject, 
    phone_number = phone_number, 
    msg = msg
  )
  files = []
  name, ext = get_ext_name(f)
  for f in rf.getlist('files'):
    file = File.objects.create(
      link=message.id,
      path=f, ext=ext, name = name,
      type=get_type(f)
    )

    files.append(file)

    mail.attach(f.name, f.read(), f.content_type)

  mail.send()
  message_obj = {
    'message': MessageSerializer(message).data,
    'files': FileSerializer(files, many=True).data
  }

  return Response(message_obj)

def send_email(instance, system, context, email_temp):
  subject = "Welcome to " + system
  from_email = "yourcompany@gmail.com"
  to_email = [instance.email]


  html_content = render_to_string(email_temp, context)
  text_content = strip_tags(html_content)  # fallback for non-HTML email clients

  email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
  email.attach_alternative(html_content, "text/html")
  email.send()

  
@api_view(['POST'])
def create_company(request):
  r = request.data
  
  with transaction.atomic():
    company_serializer = CompanySerializer(data = request.data)
    if not company_serializer.is_valid:
      return Response({'success': False, 'message': 'Invalid data', 'errors': company_serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    company = company_serializer.save()
    
    email_link = Email_Link.objects.create(email = company.email)
    wallet = Wallet.objects.create(owner_company = company)
    set_up_link = request.build_absolute_uri(reverse('create-main-admin', args=[company.link, email_link.token]))
    send_brevo_email(6, company.email, company.name, {'set_up':set_up_link, 'company_name':company.name})

  return Response({'success':True, 'message': 'Successfully created Company'})

@api_view(['POST'])
def create_main_admin(request, link, token):
  
  if not link or not token:
    return Response({'success':False, 'message': 'Link invalid'})
  
  company = Company.objects.filter(link = link).first()
  if not company: return Response({'success':False, 'message': 'Company not found'})
  
  email_link = Email_Link.objects.filter(token = token).first()
  if not email_link: return Response({'success':False, 'message': 'Link invalid'})
    
  with transaction.atomic():
    admin_serializer = EmployeeSerializer(data = request.data)
    if not admin_serializer.is_valid():
      return Response({'success': False, 'message': 'Admin is not valid', 'errors':admin_serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    try:
      department = Department.objects.get(company = company, name = 'Admin')
    except:
      department = Department.objects.create(company = company, name = 'Admin', description = 'Department of people who are administraors')
    
    permissions = Permission.objects.create(can_use_admin_system = True)
    role = Role.objects.create(name = 'Admin', company = company, department = department, permissions = permissions)
    
    admin = Employee.objects.create(company = company, department =department, role = role, **admin_serializer.validated_data)
    print('Validated Data: ', admin_serializer.validated_data)
    print('ADMIN:', admin)
    wallet = Wallet.objects.create(owner_employee = admin)

    
    admin_email_link = Email_Link.objects.create(email = admin.email)
    
    set_up = request.build_absolute_uri(reverse('set-password', args = [admin.link, admin_email_link.token]))
    send_brevo_email(7, admin.email, admin.name, {'company_name':company.name, 'user_name':admin.name, 'set_up':set_up})
  
  return Response({'success':True, 'message':'Successfully created Admin Account'})

@api_view(['POST'])
def set_password(request, link):
  employee = Employee.objects.filter(link = link).first()
  
  if not employee:
    return Response({'success': False, 'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
  
  r = request.data
  p1 = r.get('pass-1')
  p2 = r.get('pass-2')
  if not (p1 == p2):
    return Response({'success':False, 'message': 'Passwords do not match'})
  employee.set_employee_password(p1)
  request.session['emp_id'] = employee.emp_id
  request.session.cycle_key()

  return Response({'success': True, 'message':'Passwords set successfully'})

@api_view(['GET'])
def get_employees(request):
  employees = Employee.objects.all().order_by('id')
  serializer = EmployeeSerializer(employees, many=True).data

  return Response(serializer)

@api_view(['POST'])
def admin_login(request):
  r = request.data
  adm = Employee.objects.filter(emp_id = r.get('adm_id')).first()
  
  if not adm:
    return Response({'success': False, 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
  
  if not adm.role.permissions.can_use_admin_system:
    return Response({"success":False,"message": 'User does not have admin permissions'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
  
  if not check_password(r.get('password'), adm.password):
    return Response({'success':False, 'message': 'Id/Password Incorrect'})
  
  request.session['emp_id'] = adm.emp_id
  request.session.cycle_key()
  return Response({'success':True, 'message':'Successful Login'})


@api_view(['GET'])
def log_out(request):
  request.session.flush()
  return Response({'':''})

@api_view(['POST'])
def create_employee(request):
  r = request.POST
  f = request.FILES
  company = Company.objects.get(id = request.session.get('company_id'))
  
  e = Employee.objects.create(
    # --- Personal Details ---
    first_name = r.get('first_name'),
    last_name = r.get('last_name'),
    other_names = r.get('other_names'),
    gender = r.get('gender'),
    date_of_birth = r.get('date_of_birth'),

    location = r.get('location'),
    house_code = r.get('house_code'),
    marital_status = r.get('marital_status'),

    # --- Father Details ---
    father_first_name = r.get('father_first_name'),
    father_last_name = r.get('father_last_name'),
    father_date_of_birth = r.get('father_date_of_birth'),
    father_location = r.get('father_location'),
    father_marital_status = r.get('father_marital_status'),
    father_living_status = r.get('father_living_status'),

    # --- Mother Details ---
    mother_first_name = r.get('mother_first_name'),
    mother_last_name = r.get('mother_last_name'),
    mother_date_of_birth = r.get('mother_date_of_birth'),
    mother_location = r.get('mother_location'),
    mother_marital_status = r.get('mother_marital_status'),
    mother_living_status = r.get('mother_living_status'),

    # --- Contacts ---
    email = r.get('email'),
    phone_number = r.get('phone_number'),

    # --- Company Details ---
    company = company,
    department = get_object_or_404(Department, id = int(r.get('department'))),
    role = get_object_or_404(Role, id = int(r.get('role'))),
    employment_type = get_object_or_404(Employment_Type, id = int(r.get('employment_type'))),
  )
  
  pic = f.get('picture')
  
  if pic:
    e.picture = pic
    print(pic)
    e.save()
  
  wallet = Wallet.objects.create(owner_employee = e)
  
  uid = urlsafe_base64_encode(force_bytes(e.id))
  token = uuid.uuid4()
  
  set_up_link = f'http://127.0.0.1:8000/set-password/{uid}/{token}/{e.link}'
  
  send_email(e, 'RAn', {'user':e, 'company_name': 'TAS', 'set_up_link': set_up_link}, 'emails/email_2_password_generation.html')
  serializer = EmployeeSerializer(e).data
  return Response({'employee': serializer})

@api_view(['POST'])
def create_team(request):
  r = request.data
  
  company = Company.objects.get(id =request.session.get('company_id'))
  leader = Employee.objects.get(id = r.get('leader'))
  print(leader)
  team = Team.objects.create(company = company, leader = leader, name = r.get('name'))
  print(team)
  for emp in r.getlist('members'):
    print(emp)
    member = Employee.objects.get(id = emp)
    print(member)
    team.members.add(member)
  
  serializer = TeamSerializer(team)
  return Response(serializer.data)

@api_view(['POST'])
def pay_emp(request, pk):
  r = request.data

  company = Company.objects.get(id =request.session.get('company_id'))
  employee = Employee.objects.get(id = pk)

  company_wallet = company.wallet
  employee_wallet = employee.wallet

  response = transfer(company_wallet, employee_wallet, 300)
  if not response['success']:
    return Response(response)
  
  return Response({'': ''})

@api_view(['POST'])
def task_action(request):
  r = request.data
  
  task = Task.objects.get(id = r.get('task_id'))
  n = None
  if r.get('action') == 'start-task':
    start_date = datetime.fromisoformat(r.get('start_date'))
    task.start_date = timezone.make_aware(start_date)
    task.status = 'in progress'
    task.save()
    
    message = f'Task {task.id} for {task.project.title} has been marked Started by {task.assigned_to.name} as at {task.start_date}'
    title='Task Started'
    type='approve-task'
    user = task.assigned_by
    
    get_or_create_notification(task, user, title, message, type)

  elif r.get('action') == 'complete-task':
    task.status = 'completed'
    task.completed_date = timezone.make_aware(datetime.fromisoformat(r.get('end_date')))
    task.save()
    
    message = f'Task {task.id} for {task.project.title} has been marked Completed by {task.assigned_to.name} as at {task.start_date}'
    title='Task Completed'
    type='approve-task'
    user = task.assigned_by

    n = get_or_create_notification(task, user, title, message, type)
  
  s1 = TaskSerializer(task)
  s2 = NotificationSerializer(n)

  return Response({'task':s1.data, 'notification': s2.data})

@api_view(['GET'])
def get_notification(request):
  if request.session.get('emp_id'):
    e = Employee.objects.get(emp_id=request.session.get('emp_id'))
    ns = Notification.objects.filter(user = e)
    if not ns:
      return Response({'':''})
    print(request.session.items())
    def last(ns):
      c = ns.count()
      if c == 0:
        return 0
      return ns[c-1]
    
    n = last(ns)
    dif = Decimal((make_aware(datetime.now()) - n.created).total_seconds()) if n != 0 else 0
    if dif < 5:
      notification = NotificationSerializer(n)
      return Response({'notification': notification.data })
    else:
      return Response({'':''})
  else:
    return Response({'':''})
  
@api_view(['POST'])
def approve_task(request):
  r = request.data
  try:
    task = Task.objects.get(id = r.get('task_id'))
    if r.get('answer') == 'APPROVE':
      task.status = 'is_approved'
      task.remarks = r.get('remarks') if r.get('remarks') else 'No Remarks'
      task.save()

      title = 'Task Approved'
      message = f"Your task has been marked Approved by {task.assigned_by.name}. Here are your supervisor's remarks: '{task.remarks}'"

      try:
        payment = Task_Payment_Record.objects.get(
        task = task
        )
        payment.created_by = task.assigned_by
        payment.save()
        print('Task Payment Record gotten')
      except:
        payment = Task_Payment_Record.objects.create(
          task = task,
          employee = task.assigned_to
        )
        payment.created_by = task.assigned_by
        payment.save()
        print('Task Payment Record created')

      get_or_create_notification(task, task.assigned_to, title, message, 'approve-task' )
    elif r.get('answer') == 'NOT APPROVE':
      task.status = 'in progress'
      task.remarks = r.get('remarks')
      task.save()

      title = 'Task Not Approved'
      message = f"Your task has been marked Not Approved by {task.assigned_by.name}. Here are your supervisor's remarks: '{task.remarks}'"
      type = 'approve-task'
      get_or_create_notification(task, task.assigned_to, title, message, type )

    else:
      print(f'You are supposed to type APPROVE not {r.get("answer")}')
      return Response({'Error':f'You are supposed to type APPROVE not {r.get("answer")}'})

    return Response({'':''})
  except Exception as e:
    print(e)
    return Response({'Error': f'{e}'})


def get_or_create_notification(task, user, title, message, type):
  try:
    n = Notification.objects.get(user = user, task = task)
    if n.history == None:
      n.history = str(f' {n.__dict__}')
    else:
      n.history += str(f' {n.__dict__}')
    
    n.title = title
    n.message = message
    n.task = task
    n.save()

    print('😀😀 Notification Updated')
    return n
  except Notification.DoesNotExist:
    n= Notification.objects.create(user = user, message=message, title = title, type=type, task = task)
    print( '✅ Notification Created')
    return n
  
  except Exception as e:
    print('😎😎 Error, ', e)
    raise e