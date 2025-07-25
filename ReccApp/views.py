from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from GiziApp.models import Gizi
from FoodApp.models import Food
from .models import Recc
from .serializers import ReccSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_recommendation(request):
    budget = request.data.get('budget')
    people = request.data.get('people')
    days = request.data.get('days')
    user = request.user

    if not all([budget, people, days]):
        return Response({'message': 'budget, people, days harus diisi'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        budget = int(budget)
        people = int(people)
        days = int(days)
    except ValueError:
        return Response({'message': 'budget, people, days harus berupa angka'}, status=status.HTTP_400_BAD_REQUEST)

    # Buat data Gizi
    gizi = Gizi.objects.create(user=user, budget=budget, people=people, days=days)

    # Ambil semua makanan, urutkan dari harga termurah
    foods = list(Food.objects.all().order_by('price'))
    if not foods:
        return Response({'message': 'Belum ada data makanan'}, status=status.HTTP_400_BAD_REQUEST)

    reccs = []
    total_budget = budget
    for day in range(1, days + 1):
        daily_budget = budget // days
        daily_total = 0
        daily_foods = []
        for food in foods:
            if daily_total + food.price <= daily_budget:
                daily_total += food.price
                daily_foods.append(food)
        if not daily_foods:
            daily_foods = [foods[0]]
        for food in daily_foods:
            recc = Recc.objects.create(simulasi=gizi, food=food, day_number=day)
            reccs.append(recc)

    recc_serializer = ReccSerializer(reccs, many=True)
    return Response({
        'message': 'Rekomendasi makanan berhasil dibuat',
        'simulasi_id': gizi.id,
        'rekomendasi': recc_serializer.data
    }, status=status.HTTP_201_CREATED)
