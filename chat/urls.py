from django.urls import path
from . import views

urlpatterns =[
  path('chatroom/', views.chatroom, name = 'chatroom'),
  path('contact-list/', views.contact_list, name = 'contact-list'),
  path('<str:link>/', views.chat, name = 'chat'),
]