from django.test import TestCase
from charsheets.models import Character
from chat.models import ChatMessage, ChatRoom, UserBelongsToRoom
from request.models import UserToRoomRequest
from django.contrib.auth.models import User


class UserToRoomRequestTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser2', password='12345')
        testroom = ChatRoom.objects.create(name="room 1", gamemaster=testuser, status=1, description="desc 1")
        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)
        rq1 = UserToRoomRequest.objects.create(room=testroom, user=testuser, message="request 1")
        rq2 = UserToRoomRequest.objects.create(room=testroom, user=testuser2, message="request 2")
    
    def test_Request_Creation(self):
        requests = UserToRoomRequest.objects.all()
        self.assertEqual(len(requests), 2)
    
    def test_Request_Delete_OnUserDelete(self):
        user1 = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        room = ChatRoom.objects.get(name="room 1")
        requests = UserToRoomRequest.objects.all()
        self.assertEqual(len(requests), 2)
        room.gamemaster=user2
        room.save()
        user1.delete()
        requests = UserToRoomRequest.objects.all()
        self.assertEqual(len(requests), 1)

    def test_Request_Delete_OnRoomDelete(self):
        room1 = ChatRoom.objects.get(name="room 1")
        requests = UserToRoomRequest.objects.all()
        self.assertEqual(len(requests), 2)
        room1.delete()
        requests = UserToRoomRequest.objects.all()
        self.assertEqual(len(requests), 0)
    


    
