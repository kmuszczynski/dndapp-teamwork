from django.db import models
from django.contrib.auth.models import User

# Modele, absolutnie nic ciekawego

class CombatClass(models.Model):
    name = models.CharField(max_length=50)
    hit_die = models.IntegerField()

    def __str__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length=50)
    speed = models.IntegerField()

    def __str__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    
    race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True)
    combat_class = models.ForeignKey(CombatClass, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - lvl {self.level} {self.race} {self.combat_class}"


