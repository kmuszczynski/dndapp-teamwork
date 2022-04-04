from django.contrib import admin
from .models import Chat, ChatRoom, UserBelongsToRoom


admin.site.register(ChatRoom)
admin.site.register(Chat)
admin.site.register(UserBelongsToRoom)
