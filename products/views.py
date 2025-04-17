from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.core.cache import cache 
from .models import Product, Category
from .serializers import *
from rest_framework.pagination import PageNumberPagination


# Tùy Chỉnh Phân Trang cho API
class ProductPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'


# API danh sách sản phẩm (không có images)
class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = f"product_list_page_{request.query_params.get('page', 1)}"
        product_data = cache.get(cache_key)

        if product_data:
            print("🔥 Data from Redis")
        else:
            print("🗄️ Data from Database")
            products = Product.objects.all()
            paginator = ProductPagination()
            paginated_products = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(paginated_products, many=True)
            product_data = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, product_data, timeout=300)
        return Response(product_data)


# API chi tiết sản phẩm (có images)
class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        cache_key = f"product_{pk}"
        product_data = cache.get(cache_key) 

        if not product_data:
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductDetailSerializer(product)
                product_data = serializer.data
                cache.set(cache_key, product_data, timeout=300)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(product_data)


# API danh sách danh mục
class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = "category_list"
        category_data = cache.get(cache_key)

        if not category_data:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            category_data = serializer.data
            cache.set(cache_key, category_data, timeout=300)
        return Response(category_data)
