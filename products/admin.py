from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

# Admin cho Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)


# Admin cho Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'size', 'color', 'category','avatar_preview')
    search_fields = ('name__icontains', 'category__name__icontains', 'color__icontains')
    list_filter = ('size', 'category', 'created_at')
    list_editable = ( 'size',)  # Cho phép chỉnh sửa trực tiếp trong danh sách
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'stock', 'size', 'color', 'category', 'image')
        }),
    )

    def avatar_preview(self, obj):
        """Hiển thị ảnh avatar trong danh sách admin"""
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:5px;" />', obj.image.url)
        return "(Không có ảnh)"

admin.site.register(Product, ProductAdmin)



# Admin cho ProductImage
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')
    search_fields = ('product__name', 'alt_text')
    list_filter = ('product',)
    ordering = ('product',)

admin.site.register(ProductImage, ProductImageAdmin)
