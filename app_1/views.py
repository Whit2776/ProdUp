from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.paginator import Paginator
from .decorators import login_required,check_if_user_exists
# Create your views here.

import os

def get_ext_name (file_path):
  file_name, file_extension = os.path.splitext(str(file_path))
  return file_name, file_extension

def get_type (file):
  return file.content_type

@check_if_user_exists
def home(request):
  user = request.user
  context = {'user': user}
  print("🔥 Home view loaded")
  return render(request, 'home_2/index-2.html', context)

@check_if_user_exists
def about(request):
  user = request.user
  context = {'user': user}

  return render(request, 'home_2/about.html', context)

@check_if_user_exists
def contact(request):
  user = request.user
  context = {'user': user}
  r = request.POST
  rf = request.FILES
      
  return render(request, 'home_2/contact.html', context)

@check_if_user_exists
def services(request):
  user = request.user
  context = {'user': user}
  return render(request, 'services.html', context)

@check_if_user_exists
def blog_1(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/blog_1.html', context)

@check_if_user_exists
def blog_2(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/blog_2.html', context)

@check_if_user_exists
def cart(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/cart.html', context)

@check_if_user_exists
def checkout(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/checkout.html', context)

@check_if_user_exists
def coming_soon(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/coming_soon.html', context)

@check_if_user_exists
def faq(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/faq.html', context)

@login_required
def messages(request):
  user = request.user
  context = {'user': user}
  user = request.user
  return render(request, 'home_2/messages.html', context)

@check_if_user_exists
def portfolio_details(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/portfolio_details.html', context)

@check_if_user_exists
def portfolio(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/portfolio.html', context)

@check_if_user_exists
def privacy_policy(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/privacy_policy.html', context)

@check_if_user_exists
def service_details(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/service_details.html', context)

@check_if_user_exists
def services_1(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/services_1.html', context)

@check_if_user_exists
def services_2(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/services_2.html', context)

@check_if_user_exists
def shop_details(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/shop_details.html', context)

@check_if_user_exists
def shop(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/shop.html', context)

@check_if_user_exists
def sign_in(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/sign_in.html', context)

@check_if_user_exists
def sign_up(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/sign_up.html', context)

@check_if_user_exists
def single_team(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/single_team.html', context)

@check_if_user_exists
def team(request):
  user = request.user
  context = {'user': user}
  employees = Employee.objects.all().order_by('id')
  context = {'employees':employees}

  return render(request, 'home_2/team.html', context, context)

@check_if_user_exists
def terms_conditions(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/terms_conditions.html', context)

@check_if_user_exists
def testimonials(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/testimonials.html', context)

@check_if_user_exists
def not_found_404_page(request):
  user = request.user
  context = {'user': user}
  return render(request, 'home_2/404.html', context)
