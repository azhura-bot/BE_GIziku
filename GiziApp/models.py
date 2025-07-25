from django.db import models
from django.conf import settings

# Create your models here.

class Gizi(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget = models.IntegerField()
    people = models.IntegerField()
    days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.budget}"
