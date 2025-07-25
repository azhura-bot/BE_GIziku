from django.urls import path
from . import views

urlpatterns = [
    # SHOP
    path('shop/', views.shop_list_create, name='shop-list-create'),
    path('shop/<int:pk>/', views.shop_detail, name='shop-detail'),

    # PRODUCT
    path('shop/<int:shop_id>/products/', views.product_list_create, name='product-list-create'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
]
