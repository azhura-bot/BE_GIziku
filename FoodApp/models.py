from django.db import models

class Food(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo_food = models.ImageField(upload_to='images/food/', null=True, blank=True)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    nutrition = models.IntegerField()
    cook_time = models.IntegerField()
    preparation_time = models.IntegerField()
    instruction = models.TextField()
    ingridients = models.TextField()

    def __str__(self):
        return self.title
