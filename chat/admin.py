from django.contrib import admin
from .models import CharacterBelongsToRoom, Chat, ChatRoom

admin.site.register(ChatRoom)
admin.site.register(Chat)
admin.site.register(CharacterBelongsToRoom)