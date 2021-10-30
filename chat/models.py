from django.db import models
from django.contrib.auth.models import User
'''
class Message(models.Model):
    messgID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User,verbose_name="userID",on_delete=models.PROTECT)
    message = models.CharField(max_length=256)
    msgSentDate= models.TimeField(auto_now=False,auto_now_add=True)
    sessionID = models.ForeignKey(Session,verbose_name="SessionID",on_delete=models.CASCADE,null=False)

'''