from django.shortcuts import render

def check_email(request):
  return render(request, 'dashboard/check_email.html')