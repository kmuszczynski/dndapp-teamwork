from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


username_validator = UnicodeUsernameValidator()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50)
    username = forms.CharField(help_text='')
    password1 = forms.CharField(help_text='', widget=(forms.PasswordInput(attrs={'class': 'form-control'})))
    password2 = forms.CharField(help_text='', widget=(forms.PasswordInput(attrs={'class': 'form-control'})))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
