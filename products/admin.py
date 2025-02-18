from django.contrib import admin
from .models import Category, Product, ProductImage

# Admin cho Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)


# Admin cho Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'size', 'color', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category__name', 'color')
    list_filter = ('size', 'category', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock', 'size', 'color')  # Cho phép chỉnh sửa trực tiếp trong danh sách
    
    # Cập nhật lại fieldsets để loại bỏ các trường created_at và updated_at
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'stock', 'size', 'color', 'category', 'image')
        }),
    )

admin.site.register(Product, ProductAdmin)



# Admin cho ProductImage
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')
    search_fields = ('product__name', 'alt_text')
    list_filter = ('product',)
    ordering = ('product',)

admin.site.register(ProductImage, ProductImageAdmin)
