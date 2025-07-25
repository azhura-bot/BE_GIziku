from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .managers import UserManager
# Create your models here.
def generate_user_id():
    return f"USR-{uuid.uuid4()}"

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    ROLE_CHOICES = (
        ('penjual', 'penjual'),
        ('user', 'user'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        null=False,
        blank=False
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    photo_profile = models.ImageField(upload_to='iamges/profile_photos/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True) 
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # WAJIB untuk admin
    is_superuser = models.BooleanField(default=False)  # WAJIB untuk admin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
