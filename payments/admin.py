from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order__id', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ("Thông tin đơn hàng", {'fields': ('order', 'amount', 'payment_method', 'transaction_id')}),
        ("Trạng thái", {'fields': ('status',)}),
        ("Thời gian", {'fields': ('created_at', 'updated_at')}),
    )

admin.site.register(Payment, PaymentAdmin)