from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'short_comment', 'product', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    ordering = ('-created_at',)
    list_per_page = 20
    #list_editable = ('rating',)  # Cho phép chỉnh sửa số sao trực tiếp

    def short_comment(self, obj):
        """Hiển thị phần đầu của bình luận trong danh sách admin"""
        return obj.comment[:50] + "..." if obj.comment and len(obj.comment) > 50 else obj.comment
    
    short_comment.short_description = "Bình luận"

admin.site.register(Review, ReviewAdmin)