from django.core.checks import messages
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from charsheets.models import Character
from chat.models import ChatRoom

# Create your models here
class UserToRoomRequest(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField(null=True)

    class Meta:
        unique_together = ('character', 'room') 

    def __str__(self):
        return "{} ({})-> {}".format(self.character.name, self.character.user, self.room)