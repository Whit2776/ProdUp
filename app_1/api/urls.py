from django.urls import path
from app_1.api import views

urlpatterns = [
  path('post-message', views.post_message),
  path('create-company', views.create_company),
  path('get-employees', views.get_employees),
  path('log-company-in', views.admin_login),
  path('log-out', views.log_out),
  path('create-employee', views.create_employee),
  path('create-team', views.create_team),
  path('send-payment/<int:pk>', views.pay_emp),
  path('task-action', views.task_action),
  path('get-notification', views.get_notification),
  path('approve-task', views.approve_task),
  path('create-main-admin/<str:link>/<str:token>', views.create_main_admin),
  path('set-password/<str:link>', views.set_password),
  path('edit-role-permissions', views.edit_role_permissions)
]
