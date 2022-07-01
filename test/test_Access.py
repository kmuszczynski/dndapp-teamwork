from django.test import TestCase
from django.test import Client
from charsheets.models import Character
from chat.models import ChatMessage, ChatRoom, UserBelongsToRoom
from django.contrib.auth.models import User

class AccessTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        
        testroom = ChatRoom.objects.create(name="room1", gamemaster=testuser, status=1, description="desc 1")
        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)

# enter site

    def test_Home(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
    
# view profile

    def test_Anonymous_Profile(self):
        client = Client()
        response = client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/profile/')

    def test_LoggedUser_Profile(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/profile/')
        self.assertEqual(response.status_code, 200)
    
# view room content

    def test_Anonymous_Chat(self):
        client = Client()
        response = client.get('/chat/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/chat/')

    def test_LoggedUser_Chat(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/chat/')
        self.assertEqual(response.status_code, 200)

# view requests 

    def test_Anonymous_Requests(self):
        client = Client()
        response = client.get('/request/view_all')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/request/view_all')

    def test_LoggedUser_Requests(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/request/view_all')
        self.assertEqual(response.status_code, 200)
    
# list available/used rooms

    def test_Anonymous_Rooms(self):
        client = Client()
        response = client.get('/request/view_all_room')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/request/view_all_room')

    def test_LoggedUser_Rooms(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/request/view_all_room')
        self.assertEqual(response.status_code, 200)
    
# list public rooms

    def test_Anonymous_PublicRooms(self):
        client = Client()
        response = client.get('/request/allPublic/0')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/request/allPublic/0')

    def test_LoggedUser_PublicRooms(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/request/allPublic/0')
        self.assertEqual(response.status_code, 200)

# chatroom entry

    def test_Anonymous_ChatRoom(self):
        client = Client()
        response = client.get('/chat/room1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/chat/room1/')

    def test_Permitted_LoggedUser_ChatRoom(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/chat/room1/')
        self.assertEqual(response.status_code, 200)

    def test_Refused_LoggedUser_ChatRoom(self):
        client = Client()
        login = client.login(username='testuser2', password='12345')
        response = client.get('/chat/room1/')
        self.assertTemplateUsed(response, 'chat/error.html')

# create character 

    def test_Anonymous_CreateCharacter(self):
        client = Client()
        response = client.get('/character/room1/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/character/room1/create/')

    def test_LoggedUser_CreateCharacter(self):
        client = Client()
        login = client.login(username='testuser', password='12345')
        response = client.get('/character/room1/create/')
        self.assertEqual(response.status_code, 200)

