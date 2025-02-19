from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

# Admin cho Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)

# Inline cho ProductImage để có thể thêm nhiều ảnh trong Product
class ProductImageInline(admin.TabularInline):  # Hoặc admin.StackedInline để hiển thị dạng khối
    model = ProductImage
    extra = 3  # Số lượng form rỗng mặc định để upload nhiều ảnh
    fields = ('image_preview','alt_text','image',)
    readonly_fields = ('image_preview',)  # Xem trước ảnh trong admin

    def image_preview(self, obj):
        """Hiển thị ảnh preview"""
        if obj.image:
            return format_html('<img src="{}" width="150" style="border-radius:5px;" />', obj.image.url)
        return "(Không có ảnh)"

    image_preview.short_description = "Xem trước ảnh"

# Admin cho Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'size', 'color', 'category', 'avatar_preview')
    search_fields = ('name__icontains', 'category__name__icontains', 'color__icontains')
    list_filter = ('size', 'category', 'created_at')
    list_per_page = 10
    list_editable = ('size',)
    readonly_fields = ('avatar_preview_detail', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('avatar_preview_detail', 'image', 'name', 'description', 'price', 'stock', 'size', 'color', 'category', 'created_at', 'updated_at')
        }),
    )
    
    inlines = [ProductImageInline]  # Gán Inline vào ProductAdmin

    def avatar_preview(self, obj):
        """Hiển thị ảnh avatar trong danh sách admin"""
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:5px;" />', obj.image.url)
        return "(Không có ảnh)"

    def avatar_preview_detail(self, obj):
        """Hiển thị ảnh avatar chi tiết trong admin"""
        if obj.image:
            return format_html('<img src="{}" width="250" style="border-radius:5px;" />', obj.image.url)
        return "(Không có ảnh)"

admin.site.register(Product, ProductAdmin)
