from django.urls import path
from .views import get_recommendation

urlpatterns = [
    path('recc/<int:simulasi_id>/', get_recommendation, name='get-recommendation'),
] 