from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class CustomerUser(models.Model):
    GENDER_CHOICES = [
            ('male', 'Nam'),
            ('female', 'Nữ'),
            ('other', 'Khác'),
        ]

    phone_validator = RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message="Số điện thoại phải có định dạng hợp lệ (9-15 chữ số, có thể bắt đầu bằng +)."
    )

    # Thông tin cơ bản
    avatar = models.ImageField(upload_to='customers/avatars/%Y/%m/', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    email = models.EmailField(max_length=254, unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        validators=[phone_validator]
    )
    address = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Độ dài mặc định như User Django
    date_joined = models.DateTimeField(default=timezone.now)  # Ngày tạo tài khoản
    updated_at = models.DateTimeField(auto_now=True)  # Ngày cập nhật cuối
    is_active = models.BooleanField(default=True)  # Trạng thái tài khoản

    class Meta:
        verbose_name = "Khách Hàng"
        verbose_name_plural = "Khách Hàng"

    def __str__(self):
        return self.username

    @property
    def age(self):
        """Tính tuổi của khách hàng dựa trên ngày sinh"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
