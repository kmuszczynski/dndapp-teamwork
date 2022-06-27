from django.test import TestCase
from charsheets.models import Character
from chat.models import Chat, ChatRoom, UserBelongsToRoom
from django.contrib.auth.models import User

class CharacterTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser2', password='12345')
        
        testroom = ChatRoom.objects.create(name="room 1", gamemaster=testuser, status=1, description="desc 1")

        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)

        testchar2 = Character.objects.create(name="char2", level="0",race="race 2", combat_class="class 2", background="bg 2", alignment="align 2", room = testroom, user= testuser)

        testchar3 = Character.objects.create(name="char3", level="0",race="race 3", combat_class="class 3", background="bg 3", alignment="align 3", room = testroom, user= testuser)

        testchar4 = Character.objects.create(name="char4", level="0",race="race 4", combat_class="class 4", background="bg 4", alignment="align 4", room = testroom, user= testuser2)


    def test_Correct_CharacterCreation(self):
        char1 = Character.objects.get(name="char1")
        self.assertEqual(char1.name, "char1")

    def test_Incorrect_CharacterCreation_Field_Blank(self):
        user1 = User.objects.get(username="testuser")
        room1 = ChatRoom.objects.get(name="room 1")
        self.assertRaises(Exception, Character.objects.create(name="", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = room1, user= user1))

    def test_Incorrect_CharacterCreation_ArgumentNumber(self):
        try:
            self.fail(Exception, Character.objects.create(name="test"))
        except:
            pass
    
    def test_Incorrect_CharacterCreation_NoneRoom(self):
        user1 = User.objects.get(username="testuser")
        room1 = ChatRoom.objects.get(name="room 1")
        try:
            self.fail(Exception, Character.objects.create(name="char3", level="0",race="race 3", combat_class="class 3", background="bg 3", alignment="align 3", room = testroom1, user= user1))
        except:
            pass
    
    def test_Incorrect_CharacterCreation_NoneUser(self):
        user1 = User.objects.get(username="testuser")
        room1 = ChatRoom.objects.get(name="room 1")
        try:
            self.fail(Exception, Character.objects.create(name="char3", level="0",race="race 3", combat_class="class 3", background="bg 3", alignment="align 3", room = room1, user= testuser1))
        except:
            pass
    
    def test_Correct_Character_WrittenData(self):
        char1 = Character.objects.get(name="char1")
        self.assertEqual(char1.name, "char1")
        self.assertEqual(char1.level, 0)
        self.assertEqual(char1.race, "race 1")
        self.assertEqual(char1.combat_class, "class 1")
        self.assertEqual(char1.background, "bg 1")
        self.assertEqual(char1.alignment, "align 1")
        self.assertEqual(char1.room.name, "room 1")
        self.assertEqual(char1.user.username, "testuser")
        
    def test_Correct_Character_DefaultData(self):
        char1 = Character.objects.get(name="char1")
        self.assertEqual(char1.hit_dice, 0)
    
    def test_Correct_Character_List(self):
        user1 = User.objects.get(username="testuser")
        chars = Character.objects.filter(user=user1)
        self.assertEqual(len(chars), 3)

    def test_Character_Deletion(self):
        user1 = User.objects.get(username="testuser")
        chars = Character.objects.filter(user=user1)
        self.assertEqual(len(chars), 3)
        Character.objects.get(name="char2").delete()
        chars = Character.objects.filter(user=user1)
        self.assertEqual(len(chars), 2)
    
    def test_Character_Update_Integerfield(self):
        char1 = Character.objects.get(name="char3")
        self.assertEqual(char1.level, 0)
        char1.level = 3 
        char1.save()
        self.assertEqual(char1.level, 3)

    def test_Character_Update_Charfield(self):
        char1 = Character.objects.get(name="char3")
        self.assertEqual(char1.race, "race 3")
        char1.race = "updated race"
        char1.save()
        self.assertEqual(char1.race, "updated race")

    def test_Character_Delete_OnUserDelete(self):
        user1 = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        chars = Character.objects.filter(user=user1)
        self.assertEqual(len(chars), 3)
        r = ChatRoom.objects.get(name="room 1")
        r.gamemaster = user2
        r.save()
        user1.delete()
        chars = Character.objects.filter(user=user1)
        self.assertEqual(len(chars), 0)
    
    def test_Character_Delete_OnRoomDelete(self):
        room1 = ChatRoom.objects.get(name="room 1")
        chars = Character.objects.filter(room=room1)
        self.assertEqual(len(chars), 4)
        room1.delete()
        chars = Character.objects.filter(room=room1)
        self.assertEqual(len(chars), 0)