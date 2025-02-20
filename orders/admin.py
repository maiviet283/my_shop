from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment

class CartItemInline(admin.TabularInline):  # Hiển thị các sản phẩm trong giỏ hàng
    model = CartItem
    extra = 1  

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    inlines = [CartItemInline]

    def total_price(self, obj):
        return f"{obj.total_price():,.0f} VNĐ" if callable(obj.total_price) else obj.total_price
    total_price.short_description = "Tổng giá trị"

class OrderItemInline(admin.TabularInline):  # Hiển thị sản phẩm trong đơn hàng
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return f"{obj.total_price:,.0f} VNĐ" if callable(obj.total_price) else obj.total_price
    total_price.short_description = "Tổng giá trị"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'method', 'status', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('order__id', 'transaction_id')
    ordering = ('-created_at',)
