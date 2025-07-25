from rest_framework import serializers
from .models import Gizi

class GiziSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gizi
        fields = '__all__'
