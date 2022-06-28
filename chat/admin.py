from django.contrib import admin
from .models import ChatMessage, ChatRoom, UserBelongsToRoom


admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(UserBelongsToRoom)
