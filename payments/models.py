from django.db import models
from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2) # số tiền cần phải trả
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Thẻ tín dụng'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('cash_on_delivery', 'Thanh toán khi nhận hàng')
    ])
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True) # mã code
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Thanh Toán"
        verbose_name_plural = "Thanh Toán"

    def __str__(self):
        return f"Thanh toán cho đơn hàng #{self.order.id} - {self.get_status_display()}"

    def is_successful(self):
        return self.status == 'completed'
