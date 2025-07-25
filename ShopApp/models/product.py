from django.db import models
from .shop import Shop

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name_product = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expired = models.DateField()
    image_product = models.ImageField(upload_to='images/product_images/', blank=True, null=True)

    def __str__(self):
        return self.name_product
