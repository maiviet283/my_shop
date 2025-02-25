from django.contrib import admin
from django.utils.html import format_html
from .models import CustomerUser

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar_preview', 'username', 'email', 'phone_number', 'date_joined', 'is_active')
    list_filter = ('is_active', 'gender', 'date_joined')
    search_fields = ('username', 'email', 'phone_number', 'full_name')
    ordering = ['-date_joined']
    list_per_page = 20  
    readonly_fields = ('date_joined', 'updated_at', 'avatar_preview', 'avatar_preview_detail') 

    fieldsets = (
        ("Thông tin tài khoản", {
            'fields': ('username', 'email', 'password', 'is_active')
        }),
        ("Thông tin cá nhân", {
            'fields': ('avatar_preview_detail','full_name', 'date_of_birth', 'gender', 'phone_number', 'address', 'avatar',)
        }),
        ("Thời gian", {
            'fields': ('date_joined', 'updated_at')
        }),
    )

    def avatar_preview(self, obj):
        """Hiển thị ảnh avatar trong danh sách admin"""
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.avatar.url)
        return "(Không có ảnh)"

    def avatar_preview_detail(self, obj):
        """Hiển thị ảnh avatar chi tiết trong admin"""
        if obj.avatar:
            return format_html('<img src="{}" width="250" style="border-radius:5px;" />', obj.avatar.url)
        return "(Không có ảnh)"

    avatar_preview.short_description = "Avatar"
    avatar_preview_detail.short_description = "Avatar chi tiết"
