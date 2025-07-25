from django.urls import path
from .views import gizi_list_create, gizi_detail_update_delete

urlpatterns = [
    path('gizi/', gizi_list_create, name='gizi-list-create'),
    path('gizi/<int:pk>/', gizi_detail_update_delete, name='gizi-detail-update-delete'),
] 
