from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomerUser


# Lấy Toàn Bộ Thông Tin Người Dùng
class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        exclude = ['password', 'date_joined', 'updated_at', 'is_active']


# Cập Nhật Thông Tin Người Dùng (Trừ: username, email, password)
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = [
            'id', 'phone_number', 'full_name', 'avatar', 
            'date_of_birth', 'gender', 'address',
        ]

    def validate_avatar(self, value):
        """Giới hạn kích thước file avatar tối đa 1MB"""
        max_size = 1 * 1024 * 1024  # 1MB
        if value and value.size > max_size:
            raise serializers.ValidationError("File quá lớn! Kích thước tối đa là 1MB.")
        return value

    def validate_email(self, value):
        """Đảm bảo email không trùng lặp (ngoại trừ email của chính user)"""
        user = self.instance
        if CustomerUser.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email này đã được sử dụng.")
        return value

    def validate_phone_number(self, value):
        """Đảm bảo số điện thoại hợp lệ"""
        if value and not value.isdigit():
            raise serializers.ValidationError("Số điện thoại chỉ được chứa số.")
        return value

    def update(self, instance, validated_data):
        """Không cho phép cập nhật password trực tiếp"""
        validated_data.pop('password', None)  # Xóa password nếu có trong request
        return super().update(instance, validated_data)


# Đăng Ký Tài Khoản : username, email, password
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})  # Ẩn password

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password']

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

    def create(self, validated_data):
        """Mã hóa password trước khi lưu"""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


# Thay Đổi Mật Khẩu
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        """Xác minh mật khẩu cũ có chính xác không"""
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Mật khẩu cũ không chính xác.")
        return value

    def validate(self, data):
        """Xác minh new_password và confirm_password khớp nhau"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Mật khẩu xác nhận không khớp."})
        return data

    def update_password(self):
        """Cập nhật mật khẩu cho user"""
        user = self.context['request'].user
        user.password = make_password(self.validated_data['new_password'])
        user.save()
        return user