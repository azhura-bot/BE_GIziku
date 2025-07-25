from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Gizi
from .serializers import GiziSerializer
from FoodApp.models import Food
from ReccApp.models import Recc
from ReccApp.serializers import ReccSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def gizi_list_create(request):
    if request.method == 'GET': 
        gizis = Gizi.objects.all()
        serializer = GiziSerializer(gizis, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = GiziSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        # Simpan data Gizi
        gizi = serializer.save(user=user)

        # Ambil semua makanan, urutkan dari harga termurah
        foods = list(Food.objects.all().order_by('price'))
        if not foods:
            return Response({'message': 'Belum ada data makanan'}, status=status.HTTP_400_BAD_REQUEST)

        reccs = []
        for day in range(1, days + 1):
            daily_budget = budget // days
            daily_total = 0
            daily_foods = []

            for food in foods:
                if daily_total + food.price <= daily_budget:
                    daily_total += food.price
                    daily_foods.append(food)

            # Kalau tidak ada yang cukup, ambil 1 makanan termurah
            if not daily_foods:
                daily_foods = [foods[0]]

            for food in daily_foods:
                recc = Recc.objects.create(simulasi=gizi, food=food, day_number=day)
                reccs.append(recc)

        recc_serializer = ReccSerializer(reccs, many=True)

        return Response({
            'message': 'Data gizi dan rekomendasi berhasil dibuat',
            'simulasi_id': gizi.id,
            'gizi': GiziSerializer(gizi).data,
            'rekomendasi': recc_serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def gizi_detail_update_delete(request, pk):
    gizi = get_object_or_404(Gizi, pk=pk, user=request.user)  # Optional: pastikan data milik user

    if request.method == 'GET':
        serializer = GiziSerializer(gizi)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GiziSerializer(gizi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        gizi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

