from django.test import TestCase
from charsheets.models import Character
from chat.models import Chat, ChatRoom, UserBelongsToRoom
from django.contrib.auth.models import User
from django.db import IntegrityError
import datetime

class ChatRoomTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser2', password='12345')
        
        testroom = ChatRoom.objects.create(name="room 1", gamemaster=testuser, status=1, description="desc 1")

        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)

        belong1 = UserBelongsToRoom.objects.create(room=testroom,user=testuser)
        belong2 = UserBelongsToRoom.objects.create(room=testroom,user=testuser2)
    
        messages = []
        for m in ["message 1", "message 2", "message 3"]:
            messages.append(Chat.objects.create(content=m, timestamp=datetime.datetime.now(), user=testuser,room=testroom))
            messages.append(Chat.objects.create(content=m, timestamp=datetime.datetime.now(), user=testuser2,room=testroom))

    def test_Room_Creation(self):
        room1 = ChatRoom.objects.get(name="room 1")
        self.assertEqual(room1.status, 1)
    
    def test_Incorrect_RoomCreation_ArgumentNumber(self):
        try:
            self.fail(Exception, Room.objects.create(name="room"))
        except:
            pass
    
    def test_Incorrect_RoomCreation_NoneUser(self):
        try:
            self.fail(Exception, ChatRoom.objects.create(name="room", user=None, status =1 , description= "123"))
        except:
            pass

    def test_Room_Update(self):
        room1 = ChatRoom.objects.get(name="room 1")
        self.assertEqual(room1.description, "desc 1")
        self.assertEqual(room1.status, 1)
        room1.description = "123"
        room1.status = 2
        room1.save()
        self.assertEqual(room1.description, "123")
        self.assertEqual(room1.status, 2)

    def test_Incorrect_Room_Update_Status(self):
        room1 = ChatRoom.objects.get(name="room 1")
        try:
            room1.status = 3
            self.fail(Exception, room1.save())
        except:
            pass

    def test_Room_Delete_OnUserDelete(self):
        user1 = User.objects.get(username="testuser")
        room = ChatRoom.objects.get(name="room 1")
        r = ChatRoom.objects.all()
        self.assertEqual(len(r), 1)
        user1.delete()
        r = ChatRoom.objects.all()
        self.assertEqual(len(r), 0)
        
    def test_UserBelongsToRoom_Delete_OnUserDelete(self):
        user1 = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        room = ChatRoom.objects.get(name="room 1")
        b = UserBelongsToRoom.objects.all()
        self.assertEqual(len(b), 2)
        room.gamemaster=user2
        room.save()
        user1.delete()
        b = UserBelongsToRoom.objects.all()
        self.assertEqual(len(b), 1)
    
    def test_UserBelongsToRoom_Delete_OnRoomDelete(self):
        user1 = User.objects.get(username="testuser")
        room = ChatRoom.objects.get(name="room 1")
        b = UserBelongsToRoom.objects.all()
        self.assertEqual(len(b), 2)
        room.delete()
        b = UserBelongsToRoom.objects.all()
        self.assertEqual(len(b), 0)

    def test_Messages_Create(self):
        chats = Chat.objects.all()
        self.assertEqual(len(chats), 6)

    
