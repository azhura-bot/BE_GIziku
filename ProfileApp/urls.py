from django.urls import path
from ProfileApp.views import *


urlpatterns = [
    path('', GetProfile, name="get_profile"),
    path('update/', UpdateProfile, name="update_profile"),
]