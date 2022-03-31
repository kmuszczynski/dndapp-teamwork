from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.createchar, name='createchar'),
    path('character/<int:character_pk>', views.viewcharacter, name='viewcharacter'),
]