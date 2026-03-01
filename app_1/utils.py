from django.shortcuts import render

def render_dashboard(request, template_name, extra_context=None):
  context = {'company': request.company, 'employee':request.employee, 'notifications': request.notifications}
  if extra_context:
    context.update(extra_context)
  return render(request, template_name, context)
