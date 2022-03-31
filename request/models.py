from django.db import models
from django.contrib.auth.models import User
from chat.models import ChatRoom

# Create your models here
class UserToRoomRequest(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'room') 

    def __str__(self):
        return "{} -> {}".format(self.user, self.room)