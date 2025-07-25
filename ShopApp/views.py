from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Shop, Product
from .serializers import ShopSerializer, ProductSerializer

# --- SHOP VIEWS ---

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shop_list_create(request):
    if request.method == 'GET':
        shops = Shop.objects.filter(user=request.user)
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def shop_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk, user=request.user)

    if request.method == 'GET':
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- PRODUCT VIEWS ---

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_create(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, user=request.user)

    if request.method == 'GET':
        products = Product.objects.filter(shop=shop)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shop=shop)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, shop__user=request.user)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
