from django.db import models
from GiziApp.models import Gizi
from FoodApp.models import Food

class Recc(models.Model):
    simulasi = models.ForeignKey(Gizi, on_delete=models.CASCADE, related_name='reccs')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='reccs')
    day_number = models.IntegerField()

    def __str__(self):
        return f"Recc for {self.simulasi} - {self.food} (Day {self.day_number})"
