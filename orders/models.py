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

    class Meta:
        verbose_name = "Giỏ Hàng"
        verbose_name_plural = "Giỏ Hàng"

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

    class Meta:
        verbose_name = "Đơn Hàng"
        verbose_name_plural = "Đơn Hàng"

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.user.username} ({self.status})"

    @classmethod
    def create_order(cls, user):
        cart = user.cart
        if not cart.items.exists():
            return None  # Giỏ hàng trống, không thể đặt hàng

        # Tạo Order trước khi thêm sản phẩm vào
        order = cls.objects.create(user=user)

        # Thêm sản phẩm vào OrderItem
        total_price = 0
        for cart_item in cart.items.all():
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            total_price += cart_item.total_price()

        # Cập nhật total_price cho Order rồi lưu lại
        order.total_price = total_price
        order.save(update_fields=["total_price"])

        cart.clear_cart()  # Xóa các CartItem thay vì xóa giỏ hàng
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
