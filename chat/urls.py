from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_chat_room, name='chat'),
    path('<str:room_name>/', views.room, name='room'),
]