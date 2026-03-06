from django.shortcuts import render, redirect
from .models import *
from chat.models import *
from django.conf import settings
from django.core.paginator import Paginator
from .decorators import employee_login_required, login_context_required
from .utils import render_dashboard
from django.contrib.auth.hashers import make_password, check_password
import secrets
import string
from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponse
# from app_1 import transaction
from django.db import transaction
from app_1.views import get_ext_name, get_type
from datetime import timedelta

def custom_404(request, exception):
  return render(request, 'dashboard/auth-404.html')
def custom_500(request):
  return render(request, 'dashboard/auth-500.html')

@employee_login_required
def home(request):
  employee = request.employee
  company = employee.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/index.html', context)

@employee_login_required
def sales_index(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/sales-index.html', context)  

@employee_login_required
def departments(request):  
  company = request.company
  departments = Department.objects.filter(company = company)
  context = {'company':company, 'departments':departments}
  return render_dashboard(request, 'dashboard/departments.html', context)

@employee_login_required
def departments_create_department(request):  
  company = request.company

  if request.method == 'POST':
    r = request.POST
    dep = Department.objects.get_or_create(company = company, name = r.get('name'), description = r.get('description'))

    return redirect('departments-create-department')
  context = {'company':company}
  return render_dashboard(request, 'dashboard/departments-create-department.html', context)  


@employee_login_required
def departments_department(request, pk):  
  company = request.company
  department = Department.objects.get(id = pk)
  context = {'company':company}
  return render_dashboard(request, 'dashboard/departments-department.html', context)

@login_context_required('Admin')
@employee_login_required
def departments_manage_department(request):
  context = {}
  return render_dashboard(request, 'dashboard/departments-manage-department.html', context)


@employee_login_required
def roles(request):  
  company = request.company
  roles = Role.objects.filter(company = company)
  context = {'company':company, 'roles':roles}
  return render_dashboard(request, 'dashboard/roles.html', context)

@employee_login_required
def roles_create_role(request):  
  company = request.company
  departments = Department.objects.filter(company = company)

  if request.method == 'POST':
    r = request.POST
    # for key, value in r.items():
    #   print(key, value)
    # return HttpResponse(f'{r.items()}')

    role_type = r.get('type') if r.get('type') in ['Admin', 'Staff'] else False
    if not role_type:
      return HttpResponse('Role Type can only be Admin or Staff')
    department = departments.filter(id = r.get('department')).first()
    if not department:
      return HttpResponse('There is no department set')
    
    role = Role.objects.filter(department = department, company = company, type = role_type , position = r.get('position'), base_rate = r.get('base_rate')).first()
    if role:
      return HttpResponse('Role already created')
    permissions = Permission.objects.create()
    role = Role.objects.create(department = department, company = company, type = role_type , position = r.get('position'), base_rate = r.get('base_rate'), permissions = permissions)
    
    return redirect('roles-create-role')
  context = {'company':company, 'departments':departments}
  return render_dashboard(request, 'dashboard/roles-create-role.html', context)  

@employee_login_required
def roles_role(request, pk):  
  company = request.company
  department = Department.objects.get(id = pk)
  context = {'company':company}
  return render_dashboard(request, 'dashboard/roles-role.html', context)  

@employee_login_required
def employment_types(request):  
  company = request.company
  employment_types = Employment_Type.objects.get(company = company)
  context = {'company':company, 'employment_types':employment_types}
  return render_dashboard(request, 'dashboard/employment-types.html', context)

@employee_login_required
def employment_type(request, pk):  
  company = request.company
  employment_type = Employment_Type.objects.get(id = pk)
  context = {'company':company, 'employment_type':employment_type}
  return render_dashboard(request, 'dashboard/employment-type.html', context)

@employee_login_required
def employment_types_create(request):  
  company = request.company

  if request.method == 'POST':
    r = request.POST
    e_ty , created= Employment_Type.objects.get_or_create(company = company, type = r.get('type'), factor = Decimal(r.get('factor')))
    print(f'😁😁{e_ty.type} e_type Created' ) if not created else print(f'😁😁{created.type} e_type gotten')
    return redirect('employment-types-create')
  context = {'company':company}
  return render_dashboard(request, 'dashboard/employment-types-create.html', context)

@employee_login_required
def ecommerce_products(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ecommerce-products.html', context)    

@employee_login_required
def ecommerce_customers(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ecommerce-customers.html', context)    

@employee_login_required
def ecommerce_customer_details(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ecommerce-customer-details.html', context)    


@employee_login_required
def ecommerce_orders(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ecommerce-orders.html', context)    

@employee_login_required
def ecommerce_order_details(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ecommerce-order-details.html', context)    

@employee_login_required
def ecommerce_refunds(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ecommerce-refunds.html', context)    

def get_progress_tasks(company, project):
    project_tasks = Task.objects.filter(company = company, project = project)
    com = project_tasks.filter(status = 'completed').count()
    pen = project_tasks.filter(status = 'pending').count()
    
    project.progress = round(Decimal(com*100/project_tasks.count())) if project_tasks.count()> 0 else 0
    
    project.days_left = project.get_days_left()

    return project_tasks, project.progress

@employee_login_required
def projects_overview(request):
  employee = request.employee
  company = request.company
  projects = Project.objects.filter(company = company)
  for p in projects:
    get_progress_tasks(company, p)
  completed_projects = projects.filter(status = 'completed')
  tasks = Task.objects.filter(company = company)
  pending_tasks = tasks.filter(status = 'pending')
  completed_tasks = tasks.filter(status = 'completed')
  employees = Employee.objects.filter(company = company)
  active_employees = employees.filter(status = 'active')
  clients = Client.objects.filter(company = company)
  context = {'company':company, 'projects': projects, 'tasks': tasks, 'pending_tasks': pending_tasks, 'employees': employees, 'active_employees': active_employees, 'completed_tasks': completed_tasks, 'clients': clients, 'completed_projects': completed_projects}

  return render_dashboard(request, 'dashboard/projects-overview.html', context)    

# import os
# import random

# dirq = 'static/late'

# files = [f for f in os.listdir(dirq) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
# for p in Employee.objects.all():
#   file = random.choice(files)
#   print(file)
#   p.picture = f'Project-Logos/{file}'
#   p.save()
  
@employee_login_required
def projects(request):  
  company = request.company
  projects = Project.objects.filter(company = company)


  for p in projects:
    project_tasks = Task.objects.filter(company = company, project = p)

    com = project_tasks.filter(status = 'completed').count()
    pen = project_tasks.filter(status = 'pending').count()

    p.progress = round(Decimal(com*100/project_tasks.count())) if com>0 else 0

    p.days_left = p.get_days_left()
    
  context = {'company':company, 'projects':projects}
  return render_dashboard(request, 'dashboard/projects-projects.html', context)  

@employee_login_required
def project(request,pk):  
  company = request.company
  project = Project.objects.get(company = company, id =pk)
  teams = project.team.all()
  tasks = project.assigned_tasks.all()

  project_tasks = project.assigned_tasks.all()

  get_progress_tasks(company, project)

  folder = Folder.objects.get(project = project)

  if request.method == 'POST':
    r = request.POST
    f = request.FILES

    if r.get('form-name') == 'fp-form':
      if r.get('started') != '' and r.get('deadline') != '' and r.get('status') != '':
        project.started = r.get('started')
        project.deadline = r.get('deadline')
        project.status = r.get('status')
        project.save()
      return redirect('project', project.id)
    if r.get('form_name') == 'add-files-form':
      for f in f.getlist('files'):
        name, ext = get_ext_name(f)
        type = get_type(f)
        file = File.objects.create(name = name, ext = ext, type = type,  folder = folder, path=f, size=f'{ROUND_HALF_UP(Decimal(f.size)/1024)}mb')

    titles = request.POST.getlist("title[]")
    descriptions = request.POST.getlist("description[]")
    statuses = request.POST.getlist("status[]")
    priorities = request.POST.getlist("priority[]")
    # assigned_tos = request.POST.getlist("assigned_to[]")
    start_dates = request.POST.getlist("start_date[]")
    due_dates = request.POST.getlist("due_date[]")

    for i in range(len(titles)):

      if titles[i].strip() == "":
        continue 

      task = Task.objects.create(
        company = company,
        project = project,
        title = titles[i],
        description = descriptions[i],
        priority = priorities[i],
        start_date = start_dates[i],
        status = statuses[i],
        due_date = due_dates[i],
      )

      print('😂😂 Task Successfully created')
    return redirect('project', project.id)
    
  context = {'company':company, 'project':project, 'teams':teams, 'tasks':tasks, 'folder':folder }
  return render_dashboard(request, 'dashboard/project.html', context)   

@employee_login_required
def projects_board(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/projects-board.html', context)    

@employee_login_required
def projects_teams(request):  
  company = request.company
  projects = Project.objects.filter(company =company)
  teams = Team.objects.filter(company = company)
  for team in teams:
    if not team.availability:
      # try:
      project = team.assigned_project.first()
      if project:
        team_tasks = project.assigned_tasks.all()

        com = team_tasks.filter(status = 'completed').count()
        pen = team_tasks.filter(status = 'pending').count()
        total = com+pen

        team.progress = (Decimal(com) * Decimal(100) / Decimal(total)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

      else:
        pass
      
  es = Employee.objects.filter(
      company=company,
      assigned_team__isnull=True,
      assigned_teams__isnull=True
  ).distinct()

  # Potential leaders
  rl = es.filter(role__permissions__can_lead_team=True)

  # Regular employees
  re = es.exclude(role__permissions__can_lead_team=False)

  

  context = {'company':company, 'projects':projects, 'teams':teams, 'leaders':rl, 'employees':re}
  return render_dashboard(request, 'dashboard/projects-teams.html', context)    

@employee_login_required
def projects_files(request):  
  company = request.company
  folders = Folder.objects.filter(company = company)
  context = {'company':company, 'folders':folders}
  return render_dashboard(request, 'dashboard/projects-files.html', context)    

@employee_login_required
def create_projects(request):  
  company = request.company
  teams = Team.objects.filter(assigned_project__isnull = True, company = company)
  supervisors = Employee.objects.filter(supervised_projects__isnull = True, company = company, role__permissions__can_supervise = True)
  clients = Client.objects.filter(company = company)

  if request.method == 'POST':
    r = request.POST
    rf = request.FILES
    
    supervisor = r.get('supervisor')
    #employees = r.get('employees')
    team = r.get('team')
    title = r.get('title')
    client = r.get('client')
    logo = rf.get('logo')
    type = r.get('type')
    description = r.get('description')
    location = r.get('location')
    size = r.get('size')
    #status= r.get('status')
    #status_reason= r.get('status_reason')
    amount_charged = r.get('amount_charged')
    budget= r.get('budget')
    #amount_spent = r.get('amount_spent')
    started= r.get('started')
    deadline = r.get('deadline')
    #ended = r.get('ended')
    #updated = r.get('updated')
    #days_spent = r.get('days_spent')
    priority = r.get('priority')
    note= r.get('note')

    project = Project.objects.create(
      company = company,
      supervisor = Employee.objects.get(id = supervisor) if supervisor else None,
      title = title,
      client = Client.objects.get(id = int(client)),
      type = type,
      description = description,
      location = location,
      size = size,
      amount_charged = amount_charged or None,
      budget = budget or None,
      started = started or None,
      deadline = deadline or None,
      priority = priority,
      note = note,
    )

    if logo:
      project.logo = logo
      project.save()

    if int(team):
      assigned_team = Team.objects.get(id = int(team))
      project.team.add(assigned_team)

    folder = Folder.objects.create(project = project,company=company, name = project.title, description=f'Folder to host files of Project: {project.title}')
    return redirect('projects')

  context = {'company':company, 'teams':teams, 'available_supervisors':supervisors, 'clients':clients, 'today':timezone.now}
  return render_dashboard(request, 'dashboard/projects-create-project.html', context)    


@employee_login_required
def projects_create_teams(request):  
  company = request.company
  context = {'company':company, }
  return render_dashboard(request, 'dashboard/projects-create-team.html', context)   


@employee_login_required
def create_clients(request): 
  employee = request.employee 
  company = request.company
  print(company, employee)
  if request.method == 'POST':
    r = request.POST
    rf = request.FILES
    

    client = Client.objects.create(
      company = company,
      company_name = r.get('company_name'),
      name = r.get('name'),
      email = r.get('email'),
      phone_number = r.get('phone_number'),
      location = r.get('location'),
      picture = rf.get('picture'),
    )

    return redirect('clients')
    
  context = {'company':company}


  return render_dashboard(request, 'dashboard/clients-create.html', context)   

@employee_login_required
def clients(request):  
  company = request.company
  clients = Client.objects.filter(company = company)
  context = {'company':company, 'clients':clients}
  return render_dashboard(request, 'dashboard/clients.html', context)   

@employee_login_required
def client(request, pk):  
  company = request.company
  client = Client.objects.get(company=company, id = pk)
  projects = Project.objects.filter(company = company, client = client)
  context = {'company':company, 'client':client, 'projects':projects}
  return render_dashboard(request, 'dashboard/client.html', context) 

@employee_login_required
def analytics_customers(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/analytics-customers.html', context)    

@employee_login_required
def analytics_reports(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/analytics-reports.html', context)    

@employee_login_required
def apps_chat(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/apps-chat.html', context)    

@employee_login_required
def apps_contact_list(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/apps-contact-list.html', context)    

@employee_login_required
def apps_calender(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/apps-calendar.html', context)    

@employee_login_required
def apps_invoice(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/apps-invoice.html', context)    


@employee_login_required
def list_employees(request):  
  company = request.company
  employees = Employee.objects.filter(company = company.id)
  context = {'company':company, 'employees': employees}
  return render_dashboard(request, 'dashboard/employees-list.html', context)
  

@employee_login_required
def teams_employees(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/employees-teams.html', context)    

# def rename_employee_picture(instance, filename):
#     # Extract extension
#     ext = filename.name.split('.')[-1]
#     # Build new filename: e.g. John_Doe_20251005_8f3d2.jpg
#     import datetime
#     import uuid
#     import os
#     new_filename = f"{instance.first_name}_{instance.last_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.{ext}"
#     # Return the upload path
#     return os.path.join('Employee_Pictures', new_filename)

@employee_login_required
def add_employees(request):
  company = request.company
  roles = Role.objects.filter(company = company)
  departments = Department.objects.filter(company = company)
  emp_types = Employment_Type.objects.filter(company = company)

  

  # if request.method == 'POST':
  #   r = request.POST
  #   f = request.FILES
    
  #   alphabet = string.ascii_letters + string.digits + string.punctuation
  #   raw_password = ''.join(secrets.choice(alphabet) for i in range(12))

  #   hashed_password = make_password(raw_password)
    
  #   e = Employee.objects.create(
  #     # --- Personal Details ---
  #     first_name = r.get('first_name'),
  #     last_name = r.get('last_name'),
  #     other_names = r.get('other_names'),
  #     gender = r.get('gender'),
  #     date_of_birth = r.get('date_of_birth'),

  #     location = r.get('location'),
  #     house_code = r.get('house_code'),
  #     marital_status = r.get('marital_status'),

  #     # --- Father Details ---
  #     father_first_name = r.get('father_first_name'),
  #     father_last_name = r.get('father_last_name'),
  #     father_date_of_birth = r.get('father_date_of_birth'),
  #     father_location = r.get('father_location'),
  #     father_marital_status = r.get('father_marital_status'),
  #     father_living_status = r.get('father_living_status'),

  #     # --- Mother Details ---
  #     mother_first_name = r.get('mother_first_name'),
  #     mother_last_name = r.get('mother_last_name'),
  #     mother_date_of_birth = r.get('mother_date_of_birth'),
  #     mother_location = r.get('mother_location'),
  #     mother_marital_status = r.get('mother_marital_status'),
  #     mother_living_status = r.get('mother_living_status'),

  #     # --- Contacts ---
  #     email = r.get('email'),
  #     phone_number = r.get('phone_number'),

  #     # --- Company Details ---
  #     company = company,
  #     department = Department.objects.get_or_404(id = int(r.get('department'))),
  #     role = Role.objects.get_or_404(id = int(r.get('role'))),
  #     employment_type = Employment_Type.objects.get_or_404(id = int(r.get('employment_type'))),

  #     # --- Passwords ---
  #     password = hashed_password,
  #     raw_password = raw_password
  #   )

  #   if f.get('picture'):
  #     e.picture = rename_employee_picture(e, f.get('picture'))
  #     e.save()

  # else:
  #   pass


  context = {'company':company, 'roles':roles, 'departments':departments, 'emp_types':emp_types}
  return render_dashboard(request, 'dashboard/employees-add.html', context)    


@employee_login_required
def manage_employees(request):  
  company = request.company
  employees = Employee.objects.filter(company = company)
  act_emp = employees.filter(status = 'active')
  inact_emp = employees.filter(status = 'inactive')
  leave_emp = employees.filter(status = 'on leave')

  context = {'company':company, 'employees':employees, 'act_emp':act_emp, 'inact_emp':inact_emp, 'leave_emp':leave_emp}
  return render_dashboard(request, 'dashboard/employees-manage.html', context)    

@employee_login_required
def employee(request, pk):  
  company = request.company
  employee = Employee.objects.get(id = pk, company = company)
  team = employee.team.last()
  projects = []

  for p in Project.objects.filter(team = team):
    a = {'project': p, 'tasks': p.assigned_tasks.filter(assigned_to = employee)}
    projects.append(a)
  
  context = {'company':company, 'projects':projects,}
  return render_dashboard(request, 'dashboard/employee.html', context)  

@employee_login_required
def ui_alerts(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-alerts.html', context)    

@employee_login_required
def ui_avatar(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-avatar.html', context)    

@employee_login_required
def ui_buttons(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-buttons.html', context)    

@employee_login_required
def ui_badges(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-badges.html', context)    

@employee_login_required
def ui_cards(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-cards.html', context)    

@employee_login_required
def ui_carousels(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-carousels.html', context)    

@employee_login_required
def ui_dropdowns(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-dropdowns.html', context)    

@employee_login_required
def ui_grids(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-grids.html', context)    

@employee_login_required
def ui_images(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-images.html', context)    

@employee_login_required
def ui_list(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-list.html', context)    

@employee_login_required
def ui_modals(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-modals.html', context)    

@employee_login_required
def ui_navs(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-navs.html', context)    

@employee_login_required
def ui_navbar(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-navbar.html', context)    

@employee_login_required
def ui_offcanvas(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-offcanvas.html', context)    

@employee_login_required
def ui_paginations(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-paginations.html', context)    

@employee_login_required
def ui_popover_tooltips(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-popover-tooltips.html', context)    

@employee_login_required
def ui_progress(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-progress.html', context)    

@employee_login_required
def ui_spinners(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-spinners.html', context)    

@employee_login_required
def ui_tabs_accordions(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-tabs-accordions.html', context)    

@employee_login_required
def ui_typography(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-typography.html', context)    

@employee_login_required
def ui_videos(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/ui-videos.html', context)    

@employee_login_required
def advanced_animation(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-animation.html', context)    

@employee_login_required
def advanced_clip_board(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-clipboard.html', context)    

@employee_login_required
def advanced_dragula(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-dragula.html', context)    

@employee_login_required
def advanced_file_manager(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-files.html', context)    

@employee_login_required
def advanced_highlight(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-highlight.html', context)    

@employee_login_required
def advanced_range_slider(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-rangeslider.html', context)    

@employee_login_required
def advanced_ratings(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-ratings.html', context)    

@employee_login_required
def advanced_ribbons(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-ribbons.html', context)    

@employee_login_required
def advanced_sweet_alerts(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-sweetalerts.html', context)    

@employee_login_required
def advanced_toasts(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/advanced-toasts.html', context)    

@employee_login_required
def forms_basic_elements(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-basic-elements.html', context)    

@employee_login_required
def forms_advance_elements(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-advance-elements.html', context)    

@employee_login_required
def forms_validation(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-validation.html', context)    

@employee_login_required
def forms_wizard(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-wizard.html', context)    

@employee_login_required
def forms_editors(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-editors.html', context)    

@employee_login_required
def forms_file_upload(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-file-upload.html', context)    

@employee_login_required
def forms_image_crop(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/forms-img-crop.html', context)    

@employee_login_required
def charts_apex(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/charts-apex.html', context)    

@employee_login_required
def charts_justgage(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/charts-justgage.html', context)    

@employee_login_required
def charts_chatjs(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/charts-chatjs.html', context)    

@employee_login_required
def charts_toast(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/charts-toast.html', context)    

@employee_login_required
def tables_basic(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/tables-basic.html', context)    

@employee_login_required
def tables_datatables(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/tables-datatables.html', context)    

@employee_login_required
def tables_editable(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/tables-editable.html', context)    

@employee_login_required
def icons_font_awesome(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/icons-fontawesome.html', context)    

@employee_login_required
def icons_line_awesome(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/icons-lineawesome.html', context)    

@employee_login_required
def icons_icofont(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/icons-icofont.html', context)    

@employee_login_required
def icons_iconoir(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/icons-iconoir.html', context)    

@employee_login_required
def maps_google_maps(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/maps-google-maps.html', context)    

@employee_login_required
def maps_leaflet_maps(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/maps-leaflet-maps.html', context)    

@employee_login_required
def maps_vector_maps(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/maps-vector-maps.html', context)    

@employee_login_required
def email_templates_basic_action_email(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/email-templates-basic-action-email.html', context)    

@employee_login_required
def email_templates_alert_email(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/email-templates-alert-email.html', context)    

@employee_login_required
def email_templates_billing_email(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/email-templates-billing-email.html', context)    

@employee_login_required
def pages_profile(request, emp_id):  
  company = request.company
  employee = request.employee
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-profile.html', context)

@employee_login_required
def pages_notifications(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-notifications.html', context)    

@employee_login_required
def pages_timeline(request):
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-timeline.html', context)    

@employee_login_required
def pages_treeview(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-treeview.html', context)    

@employee_login_required
def pages_starter_page(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-starter.html', context)    

@employee_login_required
def pages_pricing(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-pricing.html', context)    

@employee_login_required
def pages_blogs(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-blogs.html', context)    

@employee_login_required
def pages_faqs(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-faqs.html', context)    

@employee_login_required
def pages_gallery(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/pages-gallery.html', context)    

def authentication_login(request):
  if request.method == 'POST':
    r = request.POST
    emp_id = r.get('emp_id')
    password = r.get('password')
    print('POST')
    
    employee = Employee.objects.filter(emp_id = emp_id).first()
    if not employee:
      return HttpResponse('Employee Not Found')
    
    if not check_password(password, employee.password):
      return HttpResponse('Incorrect login credentials')
    
    request.session['emp_id'] = employee.emp_id
    request.session['login_context'] = employee.role.name
    
    return redirect('projects_overview')
  return render(request, 'dashboard/auth-login-admin.html')

def authentication_register(request):
  return render(request, 'dashboard/auth-register.html')

@employee_login_required
def authentication_recover_pw(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/auth-recover-pw.html', context)    

@employee_login_required
def authentication_lock_screen(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/auth-lock-screen.html', context)    

@employee_login_required
def authentication_maintenance(request):  
  company = request.company
  context = {'company':company}
  return render_dashboard(request, 'dashboard/auth-maintenance.html', context)    

def authentication_404(request):
  return render(request, 'dashboard/auth-404.html')

def authentication_403(request):
  return render(request, 'dashboard/auth-403.html')

def authentication_500(request):
  return render(request, 'dashboard/auth-500.html')

@employee_login_required
def folders(request):
  company = request.company
  folders = Folder.objects.filter(company = company)

  context = {'folders': folders}

  return render_dashboard(request, 'dashboard/folders.html', context)

@employee_login_required
def create_folders(request):
  company = request.company
  folders = Folder.objects.filter(company = company)

  if request.method == 'POST':
    r = request.POST
    f = request.FILES
    name = r.get('name')
    description = r.get('description')
    files = f.getlist('files')

    folder = Folder.objects.create(company = company, name = name, description = description)

    for file in files:
      name, ext = get_ext_name(file)
      f = File.objects.create(company = company, path=file, ext=ext, name = name, type=get_type(file))
      f.folder = folder
      f.save()
    
    return redirect('manage-folders')
  
  context = {'folders': folders}

  return render_dashboard(request, 'dashboard/folders-create.html', context)

@employee_login_required
def folder(request, slug):
  company = request.company
  folder = Folder.objects.get(company = company, slug = slug)
  files = folder.files.all()

  context = {'folder': folder, 'files':files}

  return render_dashboard(request, 'dashboard/folder.html', context)

def authentication_staff_login(request):
  if request.method == 'POST':
    r= request.POST
    try:
      e = Employee.objects.get(emp_id = r.get('emp_id'))

      request.session['login'] = {e.emp_id}

      # if check_password(r.get('password'), e.password):
      #   request.session.flush()
      #   request.session['emp_id'] = e.emp_id

      #   if e.first_login:
      #     return redirect('change-password')

      #   
      # else: 
      #   return HttpResponse('Wrong password')
      return redirect('staff-dashboard')
    except Exception as e:
      return HttpResponse(f'Incorrect Credentials, {e}')
  return render(request, 'dashboard/auth-login.html')

@employee_login_required
def staff_change_password(request):
  emp = request.employee
  
  if request.method == 'POST':
    r= request.POST
    password = make_password(r.get('new_password'))
    emp.password = password
    emp.first_login = False
    emp.save()
    return redirect('staff-dashboard')

  return render(request, 'dashboard/auth-change-password.html')

@employee_login_required
def staff_dashboard(request):  
  company = request.company
  employee = request.employee
  context = {'company':company}
  return render_dashboard(request, 'dashboard/staff_dashboard/staff_dashboard_main.html', context)

@employee_login_required
def staff_tasks(request):  
  company = request.company
  employee = request.employee
  tasks = employee.tasks.all()
  completed = tasks.filter(status = 'completed')
  pending = tasks.filter(status = 'pending')
  not_completed = tasks.filter(status = 'not_completed')

  context = {'company':company, 'tasks':tasks, 'completed':completed, 'pending':pending, 'not_completed':not_completed}
  return render_dashboard(request, 'dashboard/staff_dashboard/staff_dashboard_tasks.html', context)


@employee_login_required
def staff_projects(request):  
  company = request.company
  employee = request.employee
  team = employee.team.last()
  projects = None
  try:
    projects = team.assigned_project.all()
  except:
    projects = employee.supervised_projects.all()

  for p in projects:
    get_progress_tasks(company, p)
  
  active = projects.filter(status = 'in_progress')
  completed = projects.filter(status = 'completed')
  pending = projects.filter(status = 'pending')

  context = {'company':company, 'team':team, 'projects':projects,'active':active,'completed':completed,'pending':pending, }
  return render_dashboard(request, 'dashboard/staff_dashboard/staff_dashboard_projects.html', context)

@employee_login_required
def staff_profile(request):  
  company = request.company
  employee = request.employee
  context = {'company':company}
  return render_dashboard(request, 'dashboard/staff_dashboard/staff-profile.html', context)

@employee_login_required
def staff_notifications(request):  
  company = request.company
  employee = request.employee
  today = timezone.now().date()
  yesterday = (timezone.now() -timedelta(days = 1)).date()
  yesterdays_back_date = (timezone.now() - timedelta(days = 2)).date()

  notifications = Notification.objects.filter(user = employee)
  todays = Notification.objects.filter(user = employee, created__date = today).order_by('-updated')
  yesterdays = Notification.objects.filter(user = employee, created__date = yesterday).order_by('-updated')
  all_other = Notification.objects.filter(user = employee, created__lt = yesterday).order_by('-updated')
  context = {'notifications':notifications, 'todays':todays,'yesterdays':yesterdays,'all_other':all_other, 'yesterdays_back_date':yesterdays_back_date}
  return render_dashboard(request, 'dashboard/staff_dashboard/staff-notifications.html', context)    

@employee_login_required
def staff_project(request,pk):  
  company = request.company
  employee = request.employee
  project = Project.objects.get(company = company, id = pk)
  teams = project.team.all()

  employee_team = employee.team.last()

  is_in_team = any(employee_team == team for team in teams)
  has_permission = employee.role.permissions.can_edit_projects

  if not has_permission and not is_in_team:
    return redirect('auth-403')
  tasks = Task.objects.filter(project = project, assigned_to = employee)

  if employee.role.permissions.can_edit_projects:
    tasks = Task.objects.filter(project = project)
  project_tasks = project.assigned_tasks.all()

  get_progress_tasks(company, project)

  folder = Folder.objects.get(project = project)

  if request.method == 'POST':
    r = request.POST
    f = request.FILES

    if r.get('form-name') == 'fp-form':
      if r.get('started') != '' and r.get('deadline') != '' and r.get('status') != '':
        project.started = r.get('started')
        project.deadline = r.get('deadline')
        project.status = r.get('status')
        project.save()
      return redirect('project', project.id)
    if r.get('form_name') == 'add-files-form':
      for f in f.getlist('files'):
        name, ext = get_ext_name(f)
        type = get_type(f)
        file = File.objects.create(name = name, ext = ext, type = type,  folder = folder, path=f, size=f'{(Decimal(f.size) / Decimal(1024)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)}mb')
      return redirect('folder', folder.slug)

    titles = request.POST.getlist("title[]")
    descriptions = request.POST.getlist("description[]")
    statuses = request.POST.getlist("status[]")
    priorities = request.POST.getlist("priority[]")
    # assigned_tos = request.POST.getlist("assigned_to[]")
    start_dates = request.POST.getlist("start_date[]")
    due_dates = request.POST.getlist("due_date[]")

    for i in range(len(titles)):

      if titles[i].strip() == "":
        continue 

      task = Task.objects.create(
        company = company,
        project = project,
        title = titles[i],
        description = descriptions[i],
        priority = priorities[i],
        start_date = start_dates[i],
        status = statuses[i],
        due_date = due_dates[i],
      )

      print('😂😂 Task Successfully created')
    return redirect('project', project.id)
    
  context = {'company':company, 'project':project, 'teams':teams, 'tasks':tasks, 'folder':folder }
  return render_dashboard(request, 'dashboard/staff_dashboard/staff-project.html', context)

def set_password(request, link, token):
  employee = Employee.objects.filter(link = link).first()
  if not employee:
    return HttpResponse('Not Found 404')
  
  email_link = Email_Link.objects.filter(token = token).first()
  if not email_link:
    return HttpResponse('Not Found 404')
  
  context = {'employee': employee}
  return render(request, 'dashboard/utils/set-password.html', context)

def create_company(request):
  return render(request, 'dashboard/create_company.html')


def create_main_admin(request, link, token):
  if not link or not token:
    return redirect('links/link_not_valid')
  
  company = Company.objects.filter(link = link).first()
  if not company: return HttpResponse('404')
  
  email_link = Email_Link.objects.filter(token = token).first()
  if not email_link: return HttpResponse('404')
  
  return render(request, 'dashboard/create_main_admin.html')