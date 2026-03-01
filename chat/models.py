from django.db import models
from app_1.models import *
from uuid import uuid4
# Create your models here.


class Chat(models.Model):
  users = models.ManyToManyField(Employee, related_name = 'chats')
  link = models.CharField(max_length=50)
  type = models.CharField(max_length = 300, null = True, default='chat')
  order = models.DateTimeField(null = True, blank = True)

  #If the chat is a group chat
  admin = models.ForeignKey(Employee, related_name='created_groups', null=True, blank = True, on_delete = models.PROTECT)
  name = models.CharField(max_length = 300, null = True, blank = True)
  def save(self, *args, **kwargs):
    if not self.link:
      self.link = str(uuid4())
      
    super().save(*args, **kwargs)
  
  def get_other_user(self, user_id):
    o = self.users.exclude(id = user_id).first()
    return o


class Mes(models.Model):
  chat = models.ForeignKey(Chat, on_delete=models.PROTECT, related_name = 'messages')
  sender = models.ForeignKey(Employee, related_name = 'sent_messages', on_delete=models.PROTECT)
  receiver = models.ForeignKey(Employee, related_name = 'received_messages', on_delete=models.PROTECT)
  message = models.TextField(null = True, blank = True)
  state = models.CharField(default = 'not delivered')
  type = models.CharField(max_length = 300, null = True, default = 'normal')
  
  #If message type = reply
  reply_to = models.PositiveIntegerField(null = True)

  created = models.DateTimeField(auto_now_add = True)
  updated = models.DateTimeField(auto_now = True)

class File(models.Model):
  company = models.ForeignKey(Company, on_delete = models.CASCADE, null=True, related_name = 'files')
  name = models.CharField(blank = True, null = True)
  path = models.FileField( upload_to='Files')
  ext = models.CharField(max_length=50, null = True)
  type = models.CharField(max_length=50, null = True)
  folder = models.ForeignKey(Folder, null = True, on_delete = models.CASCADE, related_name = 'files')
  size = models.CharField(null = True, max_length=300)
  created = models.DateTimeField(auto_now_add = True)
  message = models.ForeignKey(Mes, on_delete = models.PROTECT, null = True, related_name = 'files')

  def __str__(self):
    return f'{self.type}'