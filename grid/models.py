from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from chat.models import ChatRoom


class Grid(models.Model):
    name = models.CharField(max_length=50)
    columns = models.PositiveBigIntegerField()
    rows = models.PositiveBigIntegerField()
    status = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.columns}x{self.rows})"


class GridAreaWithCharacter(models.Model):
    column = models.PositiveBigIntegerField()
    row = models.PositiveBigIntegerField()
    grid = models.ForeignKey(Grid,on_delete=models.CASCADE)
    character = models.CharField(max_length=50)