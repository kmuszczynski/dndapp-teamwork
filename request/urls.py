from django.urls import path
from .views import *


urlpatterns = [
    path('add_user_to_room/<str:room_name>', request_add_user_to_room, name='addrequest'),
    path('view_all', view_all_request, name='viewallrequest'),
    path('more_info_about_request/<int:request_pk>', more_info_about_request_user_to_room, name='moreinfo'),
    path('view_all_room', view_all_gameroom, name="allrooms"),
    path('allPublic/<int:id_side>', all_public_room, name='allPublicRooms'),
]
