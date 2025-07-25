from django.urls import path
from .views import food_list_create, food_detail_delete, food_update

urlpatterns = [
    path('food/', food_list_create, name='food-list-create'),
    path('food/<int:pk>/', food_detail_delete, name='food-detail-delete'),
    path('food/<int:pk>/update/', food_update, name='food-update'),
] 