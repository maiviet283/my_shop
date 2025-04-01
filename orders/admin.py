from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):  # Hiển thị các sản phẩm trong giỏ hàng
    model = CartItem
    extra = 1  
    readonly_fields = ('item_total_price',)

    def item_total_price(self, obj):
        return f"{obj.total_price():,.0f} VNĐ"
    item_total_price.short_description = "Tổng tiền"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    list_per_page = 20
    search_fields = ['id','user__username','user__email','user__phone_number']
    inlines = [CartItemInline]

    def total_price(self, obj):
        return f"{obj.total_price():,.0f} VNĐ" if callable(obj.total_price) else obj.total_price
    total_price.short_description = "Tổng giá trị"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('item_total_price',)

    def has_change_permission(self, request, obj=None):
        return obj is not None  # Chỉ cho phép chỉnh sửa nếu Order đã có trong DB

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)

    def get_inlines(self, request, obj=None):
        if obj:  # Chỉ hiển thị OrderItemInline nếu Order đã có trong database
            return [OrderItemInline]
        return []

    def save_model(self, request, obj, form, change):
        """ Đảm bảo Order được lưu trước khi thêm OrderItem """
        if not obj.pk:
            obj.save()
        super().save_model(request, obj, form, change)
