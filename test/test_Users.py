from django.contrib.auth.models import User
from django.test import TestCase

class UserTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser2', password='12345')
    
    def test_Correct_User_Creation(self):
        users = User.objects.all()
        self.assertEqual(len(users), 2)