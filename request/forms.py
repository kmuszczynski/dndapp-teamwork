from django.forms import ModelForm
from .models import UserToRoomRequest


class CreateRequestAddToRoomForm(ModelForm):
    class Meta:
        model = UserToRoomRequest
        fields = ['message']
