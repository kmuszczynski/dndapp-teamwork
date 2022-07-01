from django.test import TestCase
from charsheets.models import Character
from grid.models import Grid, GridAreaWithCharacter
from chat.models import ChatMessage, ChatRoom, UserBelongsToRoom
from django.contrib.auth.models import User
from django.db import IntegrityError
import datetime

class GridTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        testuser2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser2', password='12345')
        
        testroom = ChatRoom.objects.create(name="room 1", gamemaster=testuser, status=1, description="desc 1")

        testchar1 = Character.objects.create(name="char1", level="0",race="race 1", combat_class="class 1", background="bg 1", alignment="align 1", room = testroom, user= testuser)

        grid1 = Grid.objects.create(name="grid 1", columns=10, rows=10, status=1, room=testroom)

        panel1 = GridAreaWithCharacter.objects.create(column=1,row=1,grid=grid1, character="char1", user=testuser)

    def test_Grid_Creation(self):
        grids = Grid.objects.all()
        self.assertEqual(len(grids), 1)

    def test_Grid_Correct_Update(self):
        grid = Grid.objects.get(name="grid 1")
        grid.status = 2
        grid.save()
        self.assertEqual(grid.status, 2)
    
    def test_Grid_Incorrect_Update(self):
        grid = Grid.objects.get(name="grid 1")
        try:
            grid.status = 3
            self.fail(Exception, grid.save())
        except:
            pass
        
    def test_Grid_Delete_OnRoomDelete(self):
        room1 = ChatRoom.objects.get(name="room 1")
        grids = Grid.objects.filter(room=room1)
        self.assertEqual(len(grids), 1)
        room1.delete()
        grids = Grid.objects.filter(room=room1)
        self.assertEqual(len(grids), 0)
    
    def test_Panel_Creation(self):
        panels = GridAreaWithCharacter.objects.all()
        self.assertEqual(len(panels), 1)

    def test_Panel_Correct_Update(self):
        grid1 = Grid.objects.get(name="grid 1")
        panel = GridAreaWithCharacter.objects.get(grid=grid1,column=1,row=1)
        panel.character = "updated"
        panel.save()
        self.assertEqual(panel.character, "updated")

    def test_Panel_Incorrect_Update(self):
        grid1 = Grid.objects.get(name="grid 1")
        panel = GridAreaWithCharacter.objects.get(grid=grid1,column=1,row=1)
        try:
            panel.color = "wrongcolor"
            self.fail(Exception, grid.save())
        except:
            pass

    
    




    
