from django.db import models
from customers.models import CustomerUser
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def clear_cart(self):
        self.items.all().delete()

    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    ]
    
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            super().save(*args, **kwargs)  # Lưu Order để có primary key
        self.total_price = sum(item.total_price() for item in self.items.all())
        super().save(*args, **kwargs)  # Lưu lại với total_price đã cập nhật

    
    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.user.username} ({self.status})"

    @classmethod
    def create_order(cls, user):
        cart = user.cart
        if not cart.items.exists():
            return None  # Giỏ hàng trống, không thể đặt hàng

        order = cls.objects.create(user=user, total_price=cart.total_price())
        
        for cart_item in cart.items.all():
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        
        cart.clear_cart()  # Xóa giỏ hàng sau khi đặt hàng
        return order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    
    def item_total_price(self):  # Thêm phương thức này để Django Admin có thể gọi
        return f"{self.total_price():,.0f} VNĐ"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
