from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')  # Loại bỏ các trường không muốn hiển thị

