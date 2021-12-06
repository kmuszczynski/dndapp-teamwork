from django.forms import ModelForm
from django import forms
from .models import ChatRoom

class CreateRoomForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name']