from django.db import models
from django.contrib.auth.models import User
from charsheets.models import Character
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, TextField
from django.core.validators import MaxValueValidator, MinValueValidator 

class Chat(models.Model):
    content=models.CharField(max_length=100)
    timestamp=models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey('ChatRoom', on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.timestamp, self.user)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    gamemaster = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}".format(self.name)

class CharacterBelongsToRoom(models.Model):
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    #1-active, 2-inactive, 3-dead
    status = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])

    class Meta:
        unique_together = ('character', 'room') 

    def __str__(self):
        return f"{self.room.name} ({self.character.name})"
