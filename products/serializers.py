from rest_framework import serializers
from .models import Product, Category, ProductImage

# Danh Sách Ảnh Con của một Sản Phẩm
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

# Danh Mục Sản Phẩm
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name'] 
        # đưa 2 trường lên cho frontend như vậy là đủ

# Danh Sách Sản Phẩm
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

# Danh Sách Ảnh Con của một Sản Phẩm và Thông tin của SP đó
class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True) 

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')
