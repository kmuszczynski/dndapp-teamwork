from django.core.exceptions import RequestAborted
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django.http import request
from .models import Character
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Formularz do łatwego tworzenia postaci, bardzo basic, pewnie do wywalenia

class CharacterFormChatRoom(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['user','name']

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['user']

class CharacterList(forms.Form):
    list = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        empty_label=""
    )