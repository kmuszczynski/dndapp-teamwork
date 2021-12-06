from django.db.models import fields
from django.forms import ModelForm
from django import forms
from django.forms.fields import CharField
from .models import UserToRoomRequest

class CreateRequestAddToRoomForm(ModelForm):
    class Meta:
        model = UserToRoomRequest
        fields = ['room', 'character', 'message']
