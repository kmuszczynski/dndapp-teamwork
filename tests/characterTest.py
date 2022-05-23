from django.test import TestCase
from charsheets.models import Character

class CharacterTestCase(TestCase):
    def setUp(self):
        Character.objects.create(name="lion", level="0",race="race 1", combat_class="cclass 1", background="bg 1", alignment=" align 1")
        Character.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')