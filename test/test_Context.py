from django.test import TestCase
from django.test import Client
from charsheets.models import Character
from chat.models import ChatMessage, ChatRoom, UserBelongsToRoom
from django.contrib.auth.models import User

class ContextTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        
        testroom = ChatRoom.objects.create(name="room1", gamemaster=testuser, status=1, description="desc 1")
        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)

# view room content

    def test_Chat_Context_UserData(self):
        user1 = User.objects.get(username="testuser")
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/chat/room1/')
        characters = Character.objects.get(user=user1)
        self.assertEqual(response.context['playerCharacters'][0], characters)
    
    def test_Chat_Context_RoomData(self):
        user1 = User.objects.get(username="testuser")
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/chat/room1/')
        messages = ChatMessage.objects.all()
        self.assertEqual(len(response.context['chats']), len(messages))

# view requests 

## Write tests to check if request errors get through
## Check if correct list of requests is being displayed
    
# list available/used rooms

    
# list public rooms



# chatroom entry



# create character 



