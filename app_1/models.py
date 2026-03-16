from django.db import models
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.utils.crypto import get_random_string
from uuid import uuid4
from django.contrib.auth.hashers import make_password
# Create your models here.

class User(models.Model): #User that can login in to our app to purchase things
  #Personal Details
  name = models.CharField(max_length = 500, default = '')
  first_name = models.CharField(max_length=500, null =True)
  last_name = models.CharField(max_length=500, null =True)
  other_names = models.CharField(max_length=1000, null =True)
  gender = models.CharField(max_length=100, null =True)
  date_of_birth = models.DateField(max_length = 500, null = True)
  picture = models.FileField(upload_to='Employee_Pictures', null =True)
  pic_link = models.CharField(max_length = 200000, null = True)
  location = models.CharField(max_length=10000, null =True)
  house_code = models.CharField(max_length=10000, null =True)
  #Contacts
  email = models.EmailField()
  phone_number = models.CharField(max_length=20, null =True)

  is_online = models.BooleanField(default=False)
  updated_at = models.DateTimeField(auto_now_add=True)

  status = models.CharField(max_length=100, null = True)

class Cookie(models.Model):
  employee = models.IntegerField(null = True)
  ip = models.CharField(max_length=15, null = True)

#EPR
class Company(models.Model):
  name = models.CharField(max_length=2000, null = True)
  address = models.CharField(max_length= 1000, null = True)
  email = models.EmailField()
  phone_number = models.CharField(max_length= 20, null =True)
  company_uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  link = models.CharField(max_length=60, null = True)

  first_login = models.BooleanField(default = True)

  def __str__(self):
    return f'{self.name} - {self.address} - {self.email}'
  
  def save(self, *args, **kwargs):
    if not self.link:
      self.link = str(uuid4())
    super().save(*args, **kwargs)

class Department(models.Model):
  company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name='departments')
  name = models.CharField(max_length=300)
  description = models.TextField()
  created = models.DateField(auto_now_add=True)
  updated = models.DateTimeField(auto_now = True)

  def __str__(self):
    return f'{self.company.name} - {self.name}'

class Permission(models.Model):
  can_use_admin_system = models.BooleanField(default=False)
  can_lead_team = models.BooleanField(default=False)
  can_supervise = models.BooleanField(default=False)
  can_approve_tasks = models.BooleanField(default=False)
  can_approve_payments = models.BooleanField(default=False)
  can_view_finances = models.BooleanField(default=False)
  can_assign_tasks = models.BooleanField(default=False)
  can_edit_profile = models.BooleanField(default=False)
  can_edit_tasks = models.BooleanField(default=False)
  can_edit_projects = models.BooleanField(default=False)
  can_join_team = models.BooleanField(default=False)
  can_create_projects = models.BooleanField(default = False)
  
  permission_count = models.IntegerField(default=0)
  def save(self, *args, **kwargs):
    if self.can_use_admin_system:
      self.can_approve_payments = True
      self.can_approve_tasks = True
      self.can_assign_tasks = True
      self.can_edit_profile = True
      self.can_supervise = True
      self.can_lead_team = True
      self.can_view_finances = True
      self.can_edit_tasks = True
      self.can_edit_projects = True
      self.can_create_projects = True
      
    self.permission_count = sum([
      self.can_use_admin_system,
      self.can_lead_team,
      self.can_supervise,
      self.can_approve_tasks,
      self.can_approve_payments,
      self.can_view_finances,
      self.can_assign_tasks,
      self.can_edit_profile,
      self.can_edit_tasks,
      self.can_edit_projects,
      self.can_join_team
    ])

    super().save(*args, **kwargs)
  
class Role(models.Model):
  EMPLOYEE_ROLES = [('admin', 'Admin'), ('manager', 'Manager'), ('supervisor', 'Supervisor'), ('team leader', 'Team Leader'), ('employee', 'Employee')] # And any other Custom Roles
  company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name='company_roles')
  type = models.CharField(max_length = 40, null=True) # Can only be either a staff or admin
  department = models.ForeignKey(Department, on_delete = models.PROTECT, related_name='department_roles', null = True)
  position = models.CharField(null =True,max_length = 3000, help_text = 'Position of said employees based on department/company status. Eg. Executive Officer, Department Head, Master, Technician, Helper')
  base_rate = models.DecimalField(null=True, max_digits=12, decimal_places=2, help_text = 'Base Rate for the specified role per task')
  description = models.TextField(null=True,default = 'Description of the said role')
  permissions = models.ForeignKey(Permission, on_delete = models.SET_NULL, null =True, blank = True)

  # def __str__(self):
  #   return f'{self.name} - {self.position}'

class Employment_Type(models.Model):
  EMPLOYMENT_TYPES = [('full time', 'Full Time'), ('part time', 'Part Time'), ('contract', 'Contract'), ('intern', 'Intern')]
  company = models.ForeignKey(Company, on_delete = models.CASCADE)
  type = models.CharField(max_length = 2000, help_text='Select Employee Types. Eg. Full Time,')
  factor = models.DecimalField(default = 0, max_digits=3, decimal_places=2)
  link = models.CharField(max_length = 50, null = True)

  def __str__(self):
    return f'{self.company.name} - {self.type}'

class Tool(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField(blank = True)

class Materials(models.Model):
  name = models.CharField(max_length=300)
  description = models.TextField(blank = True)

class Employee(models.Model):
  #Company Details
  EMPLOYEE_STATUS = [('active', 'Active'), ('on leave', 'On Leave'), ('inactive', 'Inactive'), ('deactivated', 'Deactivated')]

  emp_id = models.CharField(max_length = 1000, null =True, unique = True, blank=True)

  first_login = models.BooleanField(default = True)


  company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name='company_employees', null =True)
  department = models.ForeignKey(Department, on_delete = models.CASCADE, related_name='department_employees', null =True)
  role = models.ForeignKey(Role, on_delete = models.CASCADE, null = True, blank = True, related_name = 'employees')
  employment_type = models.ForeignKey(Employment_Type, on_delete = models.CASCADE, null = True, blank = True)
  performance = models.DecimalField(null = True, max_digits = 5, decimal_places = 2)

  #Personal Details
  first_name = models.CharField(max_length=500, default='', blank =True, null=True)
  last_name = models.CharField(max_length=500, default='', blank =True, null=True)
  other_names = models.CharField(max_length=1000, default='', blank =True, null=True)
  user_name = models.CharField(max_length = 1000, null =True)
  name = models.CharField(max_length = 2000, null = True, blank =True)
  gender = models.CharField(max_length=100, null =True, blank = True)
  date_of_birth = models.DateField(null=True, blank =True)
  picture = models.ImageField(upload_to='Employee_Pictures', null =True, blank = True)
  location = models.TextField( blank =True, default='', null=True)
  house_code = models.TextField( blank =True, default='', null=True)
  marital_status = models.CharField(default='',max_length=2000, blank = True, null=True)
  #Parent Info
  #Father Details
  father_first_name = models.CharField(max_length = 2000, null = True, blank =True)
  father_last_name = models.CharField(max_length = 2000, null = True, blank =True)
  father_date_of_birth = models.DateField(null = True, blank = True)
  father_location = models.TextField( blank = True, null=True)
  father_marital_status = models.CharField(max_length=2000, blank = True, null=True)
  father_living_status = models.CharField(max_length=100, blank=True, null=True)
  father_contact = models.CharField(max_length=20, blank = True, null=True)

  #Mother Details
  mother_first_name = models.CharField(max_length = 2000, null = True, blank =True)
  mother_last_name = models.CharField(max_length = 2000, null = True, blank =True)
  mother_date_of_birth = models.DateField(blank = True, null = True)
  mother_location = models.TextField( blank = True, null=True)
  mother_marital_status = models.CharField(max_length=2000, blank = True, null=True)
  mother_living_status = models.CharField(max_length=100, blank=True, null=True)
  mother_contact = models.CharField(max_length=20, blank = True, null=True)

  #Contacts
  email = models.EmailField(max_length=200, blank =True, null=True)
  phone_number = models.CharField(max_length=20, blank =True, null=True)
  #Account Details
  status = models.CharField(default='active', choices= EMPLOYEE_STATUS,max_length=100, blank= True, null=True)
  raw_password = models.CharField(default='',max_length=2000, blank = True, null=True)
  password = models.CharField(default='',max_length=2000, blank = True, null=True)
  #Mis
  updated_at = models.DateTimeField(auto_now=True)
  is_online = models.BooleanField(null = True)
  link = models.CharField(max_length = 100, null = True, blank = True)
  
  def first_three(self, value):
    value = (value or "").strip()
    return (value[:3] + "xxx")[:3]
    
  def save(self, *args, **kwargs):
    if not self.user_name:
      self.user_name = f'@{self.first_name.lower()}{get_random_string(length=5, allowed_chars='{self.last_name}0123456789')}'
      print(self.user_name)

    if not self.link:
      self.link = str(uuid4())
    if not self.emp_id:
      prefix = "EMP"
      if self.role:
        if self.role.permissions.can_use_admin_system:
          prefix = 'ADM'
        try:
          initials = (self.first_name[0] + self.last_name[0]).upper()
        except:
          initials = 'CO'
        rand = get_random_string(length=4, allowed_chars='0123456789')
        self.emp_id = f"{prefix}-{initials}-{self.first_three(self.company.name)}-{rand}"
    
    if not self.name:
      if self.last_name and self.first_name:
        self.name = f'{self.last_name} {self.other_names} {self.first_name}'.strip()
      else:
        self.name = self.user_name or 'New Employee'
    
    try:
      print("Calling super().save()...")
      super().save(*args, **kwargs)
      print("Save completed successfully")
    except Exception as e:
      print(f"ERROR during save: {e}")
      print(f"Error type: {type(e)}")
      import traceback
      traceback.print_exc()
      raise
    
  def set_employee_password(self, password):
    if not password:
      return False
    
    self.password = make_password(password)
    self.raw_password = password
    self.save(update_fields = ['password', 'raw_password'])
    return True


  
  def __str__(self):
    return f'{self.emp_id} - {self.company.name} - {self.role.position}' #- {self.company} - {self.department}'

class Email_Link(models.Model):
  email = models.EmailField()
  used = models.BooleanField(default=False)
  expired = models.BooleanField(default=False)
  expiry_date = models.DateTimeField(null=True)
  token = models.CharField(max_length = 60, null =True)
  
  def save(self, *args, **kwargs):
    if not self.token:
      self.token = str(uuid4())
    super().save(*args, **kwargs)
  
class Team(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teams')
  name = models.CharField(max_length = 100)
  leader = models.ForeignKey(Employee, on_delete = models.CASCADE, help_text='Leader must be a team leader', related_name = 'assigned_team')
  members = models.ManyToManyField(Employee, blank = True, related_name = 'team')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  availability = models.BooleanField(default=True)

class Client(models.Model):
  company = models.ForeignKey(Company, on_delete = models.CASCADE)

  company_name = models.CharField(max_length = 500, null =True)
  name = models.CharField(max_length = 300)
  email = models.EmailField()
  phone_number = models.CharField(max_length = 30)
  location = models.CharField(max_length = 300)
  status = models.CharField(max_length = 200, choices = [('active', 'Active'), ('inactive', 'Inactive')], default='active')
  picture = models.ImageField(default = 'media/default-client-image.webp')

  date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.name} - {self.location} - {self.email}'
  
class Priority(models.Model):
  PRIORITY_CHOICES = ("low", "Low"), ("moderate", "Moderate"), ("high", "High"), ("very high","Very high")
  name = models.CharField(max_length = 300)
  factor = models.DecimalField(default = 0, max_digits=5, decimal_places=4, help_text = 'By what factor should the salary of the employee be paid based on the priority of the task')

  def __str__(self):
    return f"{self.name} - {self.factor}"

class Project(models.Model):
  company = models.ForeignKey(Company, on_delete = models.CASCADE)
  supervisor = models.ForeignKey(Employee, null = True, on_delete = models.CASCADE, related_name = 'supervised_projects', blank = True)

  employees = models.ManyToManyField(Employee, related_name = 'assigned_projects', blank = True)
  #OR
  team = models.ManyToManyField(Team, related_name='assigned_project', blank = True)

  title = models.CharField(max_length = 100, null=True, blank = True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE)
  logo = models.ImageField(null = True, upload_to='Project-Logos', default = 'static/tas-logo.jpg', blank = True)
  type = models.CharField(max_length=200)
  description = models.TextField(max_length=20000, blank = True)
  location = models.CharField(max_length=10000, null = True, blank = True)
  size = models.CharField(
    max_length=100,
    choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")],
    default='unknown',
    null = True, 
    blank = True
  )

  status = models.CharField(
    max_length = 100, 
    choices=[
      ("ongoing", "Ongoing"), ("completed", "Completed"), ("pending", "Pending"), ("cancelled", "Cancelled")
      ],
    default='pending', 
    blank = True
  )
  
  status_reason = models.TextField(null =True, blank = True)

  amount_charged = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)

  budget = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)
  amount_spent = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)

  started = models.DateField(auto_now_add=True, blank = True)
  deadline = models.DateField(null=True, blank=True)
  ended = models.DateField(null=True, blank=True)
  updated = models.DateField(auto_now = True, blank = True)

  days_spent = models.PositiveIntegerField(editable=False, null = True, blank = True)

  priority =  models.CharField(
    max_length=50,
    choices=[
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ],
    default="medium"
  )

  note = models.TextField( default = '', blank = True, null = True)

  def get_days_left(self):
    if self.ended:
      return None  
    return (self.deadline - date.today()).days if self.deadline else None
  
  def __str__(self):
    return f'{self.id} - {self.title} - {self.client} - {self.status}'
  #Will populate files for this document, the invoice, reciepts, quotaions, cheques

class Task(models.Model):
  company = models.ForeignKey(Company, on_delete = models.PROTECT, related_name = 'company')

  project = models.ForeignKey(Project, on_delete = models.PROTECT, related_name='assigned_tasks')
  assigned_to = models.ForeignKey(Employee, on_delete = models.PROTECT, null = True, related_name = 'tasks')
  assigned_by = models.ForeignKey(Employee, on_delete = models.PROTECT, null = True, blank = True, related_name = 'assigned_tasks')

  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  status = models.CharField(
    max_length=50,
    choices=[
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("in progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
        ("is_approved", "Is Approved"),
        ("cancelled", "Cancelled")
    ],
    default="pending"
  )
  priority = models.ForeignKey(Priority, on_delete = models.CASCADE)

  assigned_date = models.DateTimeField(null=True, blank=True)
  start_date = models.DateTimeField(null = True, blank = True)
  due_date = models.DateTimeField(null=True, blank=True)
  completed_date = models.DateTimeField(null=True, blank=True)

  remarks = models.TextField(blank=True, null=True)
  delay_reason = models.TextField(blank=True, null=True)

  
  created_at = models.DateTimeField(auto_now_add=True, null =True)
  updated_at = models.DateTimeField(auto_now=True, null =True, blank = True)

  def mark_complete(self):
    self.completed_date == timezone.now()
    self.status = "completed"
    return f"Task '{self.title}' marked as completed."

  def remaining_days(self):
      if not self.due_date:
        return None  
      return (self.due_date - date.today()).days

  def assign_employee(self, employee):
      from app_1.models import Employee  
      if not isinstance(employee, Employee):
          raise ValueError("You must assign a valid Employee instance.")
      self.assigned_to = employee
      self.save(update_fields=["assigned_to", "updated_at"])
      return f"Task '{self.title}' assigned to {employee}."

  def record_delay(self, reason_text):
      remaining = self.remaining_days()
      if remaining is not None and remaining < 0:
        self.delay_reason = reason_text
        self.status = "on_hold"
        self.save(update_fields=["delay_reason", "status", "updated_at"])
        return f"Delay reason recorded: {reason_text}"
      return "Task is not overdue — no delay recorded."
  
  def __str__(self):
    return f'{self.id} - {self.assigned_to.name} - {self.project.client.name} - {self.project.title} - {self.status}'

class Task_Payment_Record(models.Model):
  task = models.OneToOneField(Task, on_delete=models.PROTECT)
  employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name = 'all_payment_records')
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  time_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  priority_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  paid = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  paid_at = models.DateTimeField(null=True)
  approved_by = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name = 'all_approved_payment_records', null=True)
  created_by = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name = 'all_created_payment_records', null=True)
  updated_at = models.DateTimeField(auto_now=True)

  def calculate(self):
    emp = self.employee
    task = self.task

    if not task.completed_date:
      self.amount = Decimal('0.00')
      return
    
    

    # What do i need to calculate the employee's salary
    #<----------FOR EMPLOYEE------------>
    #Employment Type and Percentage Allocated
    #Role(Role Type/Name and Position) and Base Rate
    e_type = emp.employment_type
    role = emp.role
    
    #<----------FOR TASK----------->
    #Priority
    #Due date and completed date ratio
    
    priority_factor = getattr(task.priority, 'factor', 0) or 0
    comp = timezone.localtime(task.completed_date)
    assi = timezone.localtime(task.assigned_date)
    due= timezone.localtime(task.due_date)

    used_time = comp - assi 
    total_time = due - assi

    if total_time.total_seconds() <= 0:
      self.amount = Decimal('0.00')
      print('Total time is zero')
      return

    
    ratio = Decimal(used_time.total_seconds() / total_time.total_seconds())

    
    if ratio > 1:
      time_factor = -Decimal("0.2")
    elif ratio < 0.9:
      time_factor = Decimal("0.1")
    else:
      time_factor = Decimal("0")

    self.time_factor = time_factor
    self.priority_factor = priority_factor


    self.amount = Decimal(role.base_rate*(Decimal(e_type.factor) + Decimal(priority_factor) + Decimal(time_factor)))
    self.amount = self.amount.quantize(Decimal("0.01"))

  def mark_paid(self, manager):
    self.paid = True
    self.paid_at = timezone.now()
    self.approved_by = manager
    self.save()

  def save(self, *args, **kwargs):
    if not self.paid:
      self.calculate()
    
    elif self.paid:
      self.paid_at = timezone.now()

    super().save(*args, **kwargs)

class Wallet(models.Model):
  owner = models.CharField(max_length =1000, null = True)
  owner_employee = models.OneToOneField(Employee, on_delete=models.PROTECT, related_name = 'wallet', null =True)
  owner_company = models.OneToOneField(Company, on_delete=models.PROTECT, related_name = 'wallet', null =True)
  balance = models.DecimalField(max_digits = 20, decimal_places = 4, default='0')
  currency = models.CharField(max_length = 50, default = 'GHC')
  updated = models.DateTimeField(auto_now = True)
  daily_limit = models.DecimalField(max_digits = 10, decimal_places = 4, default = 5000)
  daily_spent = models.DecimalField(max_digits = 10, decimal_places = 4, default = 0)
  minimum_balance = models.DecimalField(max_digits = 10, decimal_places = 4, default=50)
  
  chances = models.PositiveIntegerField(default= 0)
  #STATES
  is_active = models.BooleanField(default = True)
  is_flagged = models.BooleanField(default = False)
  is_frozen = models.BooleanField(default = False)
  is_suspended = models.BooleanField(default = False)
  
  def __str__(self):
    return f"{self.id} - {self.owner}'s Wallet"

  def save(self, *args, **kwargs):
    if not self.owner_company:
      self.owner = self.owner_employee.name
    else:
      self.owner = self.owner_company.name

    
    super().save(*args, **kwargs)

class Transaction(models.Model):
  wallet = models.ForeignKey(Wallet, on_delete = models.PROTECT)
  amount = models.DecimalField(max_digits = 20, decimal_places = 4)
  transaction_type = models.CharField(max_length = 30, choices = [('CREDIT', 'credit'), ('DEBIT', 'debit')])
  reference = models.CharField(max_length = 50, db_index=True)
  description = models.TextField()
  created = models.DateTimeField(auto_now_add = True)
  status = models.CharField(max_length = 100)
  before_balance = models.DecimalField(max_digits = 20, decimal_places = 4)
  after_balance = models.DecimalField(max_digits = 20, decimal_places = 4)
  updated = models.DateTimeField(auto_now = True)

class Clock_In_Record(models.Model):
  pass

class Clock_Out_Record(models.Model):
  pass

class Teamplate(models.Model):
  key = models.CharField(max_length = 40, null =True, blank = True)
  employee = models.ForeignKey(Employee, on_delete = models.PROTECT)
  name = models.CharField(max_length = 400, null =True, blank = True)
  json_schema = models.JSONField()
  created = models.DateTimeField(auto_now_add = True)
  updated = models.DateTimeField(auto_now = True)


class Message(models.Model):
  company = models.ForeignKey(Company, related_name = 'company_messages', null = True, on_delete = models.SET_NULL)
  name = models.CharField(max_length=100)
  email = models.EmailField()
  subject = models.CharField(max_length=150)
  phone_number = models.CharField(max_length=20)
  msg = models.CharField(max_length=20000)
  created = models.DateTimeField(auto_now=True)

class Folder(models.Model):
  company = models.ForeignKey(Company, on_delete = models.CASCADE, null=True, related_name = 'folders')
  name = models.CharField(max_length = 200, default='Folder')
  description = models.TextField(help_text='Description of the folder')
  created = models.DateTimeField(auto_now_add = True)
  updated = models.DateTimeField(auto_now = True)
  slug = models.CharField(max_length = 50, null=True)
  project = models.OneToOneField(Project, null =True, on_delete = models.CASCADE, related_name = 'folder')

  def save(self, *args, **kwargs):
    self.slug = uuid4()
    super().save(*args, **kwargs)

  def __str__(self):
    return f'{self.slug} - {self.name}'

class Notification(models.Model):
  user = models.ForeignKey(Employee, on_delete=models.CASCADE)
  title = models.CharField(max_length=200, default='New Message')
  message = models.TextField( default='You  have recieved a Message')
  type = models.CharField(max_length=100, default = 'normal')
  task = models.ForeignKey(Task, on_delete = models.PROTECT, null=True, blank = True)

  history = models.JSONField(null = True, blank = True)

  created = models.DateTimeField(auto_now_add = True)
  updated = models.DateTimeField(auto_now = True)
