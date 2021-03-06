from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from chat.models import ChatRoom

# Modele, absolutnie nic ciekawego

class Character(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()

    race = models.CharField(max_length=100, null=True, blank=True)
    combat_class = models.CharField(max_length=100, null=True, blank=True)
    background = models.CharField(max_length=100, null=True, blank=True)
    alignment = models.CharField(max_length=100, null=True, blank=True)

    exp = models.IntegerField(default=0)

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    main_strength = models.IntegerField(default=0)
    main_dexterity = models.IntegerField(default=0)
    main_constitution = models.IntegerField(default=0)
    main_intelligence = models.IntegerField(default=0)
    main_wisdom = models.IntegerField(default=0)
    main_charisma = models.IntegerField(default=0)

    inspiration = models.IntegerField(default=0)
    proficiencybonus = models.IntegerField(default=0)

    saving_strength = models.IntegerField(default=0)
    saving_dexterity = models.IntegerField(default=0)
    saving_constitution = models.IntegerField(default=0)
    saving_intelligence = models.IntegerField(default=0)
    saving_wisdom = models.IntegerField(default=0)
    saving_charisma = models.IntegerField(default=0)

    armorclass = models.IntegerField(default=0)
    initiative = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)

    current_hp = models.IntegerField(default=0)
    temporary_hp = models.IntegerField(default=0)

    hit_dice = models.IntegerField(default=0)

    deathsaves_success = models.IntegerField(default=0, validators=[MaxValueValidator(3)])
    deathsaves_failure = models.IntegerField(default=0, validators=[MaxValueValidator(3)])

    # skills
    acrobatics = models.IntegerField(default=0)
    animalhandling = models.IntegerField(default=0)
    arcana = models.IntegerField(default=0)
    athletics = models.IntegerField(default=0)
    deception = models.IntegerField(default=0)
    history = models.IntegerField(default=0)
    insight = models.IntegerField(default=0)
    intimidation = models.IntegerField(default=0)
    investigation = models.IntegerField(default=0)
    medicine = models.IntegerField(default=0)
    nature = models.IntegerField(default=0)
    perception = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    persuation = models.IntegerField(default=0)
    religion = models.IntegerField(default=0)
    sleightofhand = models.IntegerField(default=0)
    stealth = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    passive_wisdom = models.IntegerField(default=0)

    equipment = models.TextField(default="",max_length=300)
    proficiencies = models.TextField(default="",max_length=300)
    

    def __str__(self):
        return f"{self.name} - lvl {self.level} {self.race} {self.combat_class}"
