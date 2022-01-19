from django.urls import path

from . import views

urlpatterns = [
    path('add_user_to_room/<str:room_name>', views.request_add_user_to_room, name='addrequest'),
    path('view_all', views.viewAllRequest, name='viewallrequest'),
    path('more_info_about_request/<int:request_pk>', views.more_info_about_request_user_to_room, name='moreinfo'),
    path('view_all_room', views.view_all_gameroom, name="allrooms"),
    path('allPublic/<int:id_side>', views.all_public_room, name='allPublicRooms'),
]