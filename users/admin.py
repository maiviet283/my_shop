from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'role', 'is_staff', 'is_active') # avatar_preview
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('id',)
    
    # khi xem thông tin chi tiết user
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {'fields': ('phone_number', 'avatar', 'role', 'avatar_preview')}),
    )

    # khi tạo mới user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {'fields': ('phone_number', 'avatar', 'role')}),
    )

    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        """Hiển thị ảnh đại diện trong trang Admin."""
        if obj.avatar:
            return format_html('<img src="{}" width="210" style="border-radius: 10px;"/>', obj.avatar.url)
        return "(Chưa có ảnh)"
    
    avatar_preview.short_description = "Ảnh đại diện"

admin.site.register(CustomUser, CustomUserAdmin)
