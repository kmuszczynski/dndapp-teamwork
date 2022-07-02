from django.test import TestCase
from django.test import Client
from charsheets.models import Character
from request.models import UserToRoomRequest
from grid.models import Grid, GridAreaWithCharacter
from chat.models import ChatMessage, ChatRoom, UserBelongsToRoom
from django.contrib.auth.models import User

class ContextTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        testuser3 = User.objects.create_user(username='testuser3', password='12345')
        
        
        testroom = ChatRoom.objects.create(name="room1", gamemaster=testuser, status=1, description="desc 1")
        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)

        req = UserToRoomRequest.objects.create(room=testroom,user=testuser2,message="msg")

        belong = UserBelongsToRoom.objects.create(room=testroom,user=testuser3)

        grid1 = Grid.objects.create(name="grid 1", columns=10, rows=10, status=1, room=testroom)

        panel1 = GridAreaWithCharacter.objects.create(column=1,row=1,grid=grid1, character="char1", user=testuser)

# view requests 

    def test_Requests_List(self):
        user1 = User.objects.get(username="testuser")
        room1 = ChatRoom.objects.get(name="room1")
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/request/view_all')
        reqs = UserToRoomRequest.objects.filter(room=room1)
        self.assertEqual(response.context['requests'][0], reqs[0])


## Write tests to check if request errors get through
    
# list available/used rooms
    def test_Rooms_List(self):
        user1 = User.objects.get(username="testuser3")
        room1= ChatRoom.objects.get(name="room1")
        client = Client()
        login = client.login(username='testuser3', password='12345')
        response = client.get('/request/view_all_room')
        rooms = UserBelongsToRoom.objects.filter(user=user1, room=room1)
        self.assertEqual(response.context['player_rooms'][0], rooms[0])
    
# list public rooms

    def test_PublicRooms_List(self):
        user1 = User.objects.get(username="testuser2")
        client = Client()
        login = client.login(username='testuser2', password='12345')
        response = client.get('/request/allPublic/0')
        rooms = ChatRoom.objects.all()
        self.assertEqual(response.context['rooms'][0], rooms[0])

# create character 

    def test_Update_Character(self):
        user1 = User.objects.get(username='testuser')
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/character/update/1')
        char = Character.objects.filter(user=user1)
        self.assertEqual(response.context['character'], char[0])


