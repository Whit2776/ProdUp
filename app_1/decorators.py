from django.shortcuts import render, redirect
from .models import Company, User, Employee, Notification

def admin_login_required(view_func):
  def wrapper(request, *args, **kwargs):
    adm = request.session.get('adm_id')

    if not adm :
      return redirect('auth-staff-login')
    
    company = Company.objects.get(company_employees__emp_id = adm)
    employee = Employee.objects.get(emp_id = adm)
    notifications = Notification.objects.filter(user = employee)
    request.notifications = notifications
    request.company = company 
    request.employee = employee
    print(request.session.items())
    return view_func(request, *args, **kwargs)
  return wrapper

def login_context_required(required_context):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get('login_context') != required_context:
                return redirect(f'{required_context}_login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def employee_login_required(view_func):
  def wrapper(request, *args, **kwargs):
    emp_id = request.session.get('emp_id')
    if not emp_id:
      return redirect('auth-staff-login')
    
    notifications = Notification.objects.filter(user = Employee.objects.get(emp_id = emp_id))
    request.notifications = notifications
    return view_func(request, *args, **kwargs)
  
  return wrapper



def login_required(view_func):
  def wrapper(request, *args, **kwargs):
    id = request.session.get('user_id')
    if not id:
        return redirect('home_2/sign_in.html')
    user = User.objects.get(id = id)
    request.user = user
    return view_func(request, *args, **kwargs)
  return wrapper

def check_if_user_exists(view_func):
  def wrapper(request, *args, **kwargs):
    id = request.session.get('user_id')
    
    try:
      user = User.objects.get(id = id)
    except:
      user = None
    
    request.user = user
    
    return view_func(request, *args, **kwargs)
  return wrapper