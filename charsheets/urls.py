from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_character, name='create_character'),
    path('character/<int:character_pk>', views.view_character, name='view_character'),
]
