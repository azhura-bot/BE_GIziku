from rest_framework import serializers
from .models import Recc

class ReccSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recc
        fields = '__all__' 