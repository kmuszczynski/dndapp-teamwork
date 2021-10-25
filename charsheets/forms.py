from django.forms import ModelForm
from .models import Character
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Formularz do łatwego tworzenia postaci, bardzo basic, pewnie do wywalenia

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'level', 'combat_class']