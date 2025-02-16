from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import os

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Nhân viên'),
        ('customer', 'Khách hàng'),
    )

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Số điện thoại phải có định dạng hợp lệ (9-15 chữ số)."
    )
    
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        unique=True, 
        validators=[phone_validator]
    )
    avatar = models.ImageField(upload_to='users/avatars/%Y/%m/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    class Meta:
        verbose_name = "Người Dùng"
        verbose_name_plural = "Danh Sách Người Dùng"

    def save(self, *args, **kwargs):
        """Tự động xóa ảnh cũ khi cập nhật avatar mới"""
        try:
            old_user = CustomUser.objects.get(id=self.id)
            if old_user.avatar and old_user.avatar != self.avatar:
                if os.path.isfile(old_user.avatar.path):
                    os.remove(old_user.avatar.path)  # Xóa ảnh cũ
        except CustomUser.DoesNotExist:
            pass  # Trường hợp tạo mới user, không cần xóa ảnh

        super().save(*args, **kwargs)  # Lưu user mới

    def delete(self, *args, **kwargs):
        """Tự động xóa avatar khi user bị xóa"""
        if self.avatar and os.path.isfile(self.avatar.path):
            os.remove(self.avatar.path)  # Xóa ảnh trên ổ cứng
        super().delete(*args, **kwargs)  # Xóa user

    def __str__(self):
        return self.email if self.email else self.username
