from django.forms import ModelForm
from .models import Character

# Formularz do łatwego tworzenia postaci, bardzo basic, pewnie do wywalenia

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'level', 'combat_class']