from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Food
from .serializers import FoodSerializer
import os

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def food_list_create(request):
    if request.method == 'GET':
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        if 'photo_food' in request.FILES:
            data['photo_food'] = request.FILES['photo_food']
        serializer = FoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def food_detail_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def food_update(request, pk):
    food = get_object_or_404(Food, pk=pk)
    data = request.data.copy()
    if 'photo_food' in request.FILES:
        # Hapus file lama jika ada
        if food.photo_food:
            old_path = food.photo_food.path
            if os.path.exists(old_path):
                os.remove(old_path)
        data['photo_food'] = request.FILES['photo_food']
    serializer = FoodSerializer(food, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
