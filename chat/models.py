from django.db import models
from django.contrib.auth.models import User
from charsheets.models import Character
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, TextField

class Chat(models.Model):
    content=models.CharField(max_length=100)
    timestamp=models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey('ChatRoom', on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.timestamp, self.user)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    #on_delete zależy od tego czy damy możliwość usunięcia użytkownika do zmiany !!!!
    gamemaster = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    #Fajna opcja do przemyślenia na później
    #player_list = models.ManyToManyField(Character, related_name='room', blank=True)
    #request_list = models.ManyToManyField(Character, related_name='request', blank=True)

    def __str__(self):
        return "{}".format(self.name)

class CharacterBelongsToRoom(models.Model):
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room.name} ({self.character.name})"
