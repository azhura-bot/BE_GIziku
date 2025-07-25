from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokos')
    name_shop = models.CharField(max_length=100)
    address = models.TextField()

    def total_product(self):
        return self.produks.count()

    def __str__(self):
        return self.nama_toko
