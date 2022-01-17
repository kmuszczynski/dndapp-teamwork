from django.contrib import admin
from .models import Character, CombatClass, Race, Background, Alignment

# Admin, tyż nic.

# Register your models here.
admin.site.register(Character)
admin.site.register(CombatClass)
admin.site.register(Race)
admin.site.register(Background)
admin.site.register(Alignment)
