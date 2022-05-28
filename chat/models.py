from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import TextField
from django.core.validators import MaxValueValidator, MinValueValidator 


class Chat(models.Model):
    content = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.timestamp, self.user)


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    gamemaster = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    #1-public, 2-private
    status = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    description = TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class UserBelongsToRoom(models.Model):
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'room')
    
    def __str__(self):
        return f"{self.user} ({self.room.name})"
