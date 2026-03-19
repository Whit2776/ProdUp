from rest_framework.serializers import ModelSerializer
from app_1.models import *
from chat.models import *

class MessageSerializer(ModelSerializer):
  class Meta:
    model = Message
    fields = '__all__'

class FileSerializer(ModelSerializer):
  class Meta:
    model = File
    fields = '__all__'

class EmployeeSerializer(ModelSerializer):
  class Meta:
    model = Employee
    exclude = ['employment_type', 'department', 'role']
    # exclude = ['company', 'user_name', 'department']


class RoleSerializer(ModelSerializer):
  class Meta:
    model = Role
    fields = '__all__'

    
class CompanySerializer(ModelSerializer):
  class Meta:
    model = Company
    fields = '__all__'

class TeamSerializer(ModelSerializer):
  class Meta:
    model = Team
    fields = '__all__'

class TaskSerializer(ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'

class NotificationSerializer(ModelSerializer):
  class Meta:
    model = Notification
    fields = '__all__'
