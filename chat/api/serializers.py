from rest_framework.serializers import ModelSerializer
from chat.models import *

class MesSerializer(ModelSerializer):
  class Meta:
    model = Mes
    fields = '__all__'