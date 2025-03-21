from django.urls import path
from .import views

urlpatterns = [
    path('generate-qr/', views.generate_qr, name='generate_qr'),  # Không có đối số
    path('generate-qr/<int:amount>/', views.generate_qr, name='generate_qr_amount'),  # Chỉ có amount
    path('generate-qr/<int:amount>/<str:note>/', views.generate_qr, name='generate_qr_full'),  # Đủ cả 2
]
