from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, TextField
from django.contrib.auth.models import User
'''
class Message(models.Model):
    messgID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User,verbose_name="userID",on_delete=models.PROTECT)
    message = models.CharField(max_length=256)
    msgSentDate= models.TimeField(auto_now=False,auto_now_add=True)
    sessionID = models.ForeignKey(Session,verbose_name="SessionID",on_delete=models.CASCADE,null=False)

'''

class Chat(models.Model):
    content=models.CharField(max_length=100)
    timestamp=models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey('ChatRoom', on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.timestamp, self.user)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)
