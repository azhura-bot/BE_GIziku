from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from UserApp.models import User

# Serializer ini berfungsi untuk mengubah data model User menjadi format JSON yang bisa digunakan dalam API
# dan juga untuk memvalidasi data yang diterima dari request.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)  # ✅ Tambahkan write_only untuk password
    class Meta:
        model= User
        fields = '__all__'
    

    def create(self, validated_data):
        # ✅ Hash password saat create
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Email must contain '@' symbol")
        if '.' not in value.split('@')[-1]:
            raise serializers.ValidationError("Email must contain a valid domain extension")
        return value

    def validation_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Phone number must be between 10 and 15 digits")
        return value

    def validate_role(self, value):
        valid_roles = ['admin', 'user']
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of: {valid_roles}")
        return value
    
    def validate(self, data):
        if data.get('role') == 'admin' and not data.get('email').endswith('@company.com'):
            raise serializers.ValidationError("Admin must use company email")
        return data