from django.urls import path
from . import views


urlpatterns = [
    path('<str:room_name>/create/', views.create_character, name='create_character'),
    path('update/<int:character_pk>', views.view_character, name='view_character'),
    path('download/<int:character_pk>', views.download_character_as_json, name='download_character')
]
