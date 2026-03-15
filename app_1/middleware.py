from app_1.models import Employee

class EmployeeAuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Default: user is not logged in
    request.employee = None
    request.company = None
    request.role = None

    # Get member_id from session
    emp_id = request.session.get('emp_id')

    if emp_id:
      # Fetch member from DB if active
      employee = Employee.objects.filter(emp_id=emp_id).first()
      if employee:
        request.company = employee.company
        request.employee = employee
        request.role = employee.role
    # Continue processing the request
    print('Middleware Activated')
    print(request.session.items())
    response = self.get_response(request)
    return response