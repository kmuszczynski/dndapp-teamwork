from django.contrib import admin
from .models import Character, CombatClass, Race

# Admin, tyż nic.

# Register your models here.
admin.site.register(Character)
admin.site.register(CombatClass)
admin.site.register(Race)
