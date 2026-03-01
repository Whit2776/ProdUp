from django.urls import path
from chat.api import views

urlpatterns = [
  path('post-message/<str:link>', views.post_message),
  path('get-messages/<str:link>/<int:num>', views.get_messages),
  path('get-message/<str:link>', views.get_message),
  path('delete-message', views.delete_message),
]
