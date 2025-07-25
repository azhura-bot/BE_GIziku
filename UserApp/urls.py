from django.urls import path
from UserApp.views.auth_user import Login, Register

urlpatterns = [
    path('login/', Login, name="login"),
    path('register/', Register, name="register"),
]