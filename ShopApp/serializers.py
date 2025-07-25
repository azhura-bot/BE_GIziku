from rest_framework import serializers
from .models import Shop, Product

class ShopSerializer(serializers.ModelSerializer):
    total_product = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name_shop', 'address', 'total_product']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'shop',
            'name_product',
            'description',
            'category',
            'price',
            'expired',
            'image_product'
        ]
