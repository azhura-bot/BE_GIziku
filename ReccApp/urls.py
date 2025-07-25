from django.urls import path
from .views import create_recommendation

urlpatterns = [
    path('recc/', create_recommendation, name='create-recommendation'),
] 