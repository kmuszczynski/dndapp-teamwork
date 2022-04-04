from email.policy import default
from random import choice
from tkinter import Widget
from django.forms import ModelForm
from django import forms
from .models import ChatRoom


STATUS = (
    ("PRIVATE", "Private"),
    ("PUBLIC", "Public"),
)


class CreateRoomForm(ModelForm):
    status = forms.ChoiceField(choices=STATUS, initial="PUBLIC")
    class Meta:
        model = ChatRoom
        fields = ['name', 'description']
