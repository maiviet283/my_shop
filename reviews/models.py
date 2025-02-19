from django.db import models
from customers.models import CustomerUser
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)  # khách hàng
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} ⭐") for i in range(1, 6)],
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],  
        help_text="Chọn số sao từ 1 đến 5"
    )
    comment = models.TextField(blank=True, null=True, help_text="Nhập bình luận của bạn (không bắt buộc).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Đánh Giá Sản Phẩm"
        verbose_name_plural = "Danh Sách Đánh Giá Sản Phẩm"
        ordering = ['-created_at']
        unique_together = ('product', 'user')  # Ràng buộc mỗi user chỉ được đánh giá một sản phẩm một lần

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"
