from django.urls import path
from .views import generate_qr

urlpatterns = [
    path('generate-qr/<int:amount>/<str:note>/', generate_qr, name='generate_qr'),
]
