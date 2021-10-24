from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu', views.menu, name='menu'),
    path('create/', views.createchar, name='createchar'),
    path('character/<int:character_pk>', views.viewcharacter, name='viewcharacter'),
]