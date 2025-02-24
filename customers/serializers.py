from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomerUser

class CustomerUserSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()  # Không cho người dùng nhập, chỉ để đọc
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})  # Ẩn password

    class Meta:
        model = CustomerUser
        fields = [
            'id', 'username', 'email', 'phone_number', 'full_name',
            'avatar', 'date_of_birth', 'gender', 'address',
            'date_joined', 'updated_at', 'is_active', 'age', 'password'
        ]
        read_only_fields = ['id', 'date_joined', 'updated_at', 'is_active']  # Các field chỉ đọc

    def validate_email(self, value):
        """Đảm bảo email không trùng lặp"""
        if CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email này đã được sử dụng.")
        return value

    def validate_username(self, value):
        """Đảm bảo username không chứa ký tự đặc biệt"""
        if not value.isalnum():
            raise serializers.ValidationError("Username chỉ được chứa chữ và số.")
        return value

    def validate_phone_number(self, value):
        """Đảm bảo số điện thoại hợp lệ"""
        if value and not value.isdigit():
            raise serializers.ValidationError("Số điện thoại chỉ được chứa số.")
        return value

    def create(self, validated_data):
        """Mã hóa password trước khi lưu"""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Không cho phép cập nhật password trực tiếp"""
        if 'password' in validated_data:
            validated_data.pop('password')  # Xóa password khỏi dữ liệu update
        return super().update(instance, validated_data)
