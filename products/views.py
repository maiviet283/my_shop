from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Product, Category
from .serializers import *

# API chung cho tất cả các API
# Các API dưới đều sử dụng GET để lấy thông tin
class CustomAPIView(generics.GenericAPIView):
    """ -> Chặn tất cả phương thức không hợp lệ """
    
    def method_not_allowed(self, request, *args, **kwargs):
        return Response(
            {"error": "Phương thức không được hỗ trợ. Vui lòng sử dụng GET."}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request, *args, **kwargs):
        return self.method_not_allowed(request)

    def put(self, request, *args, **kwargs):
        return self.method_not_allowed(request)

    def delete(self, request, *args, **kwargs):
        return self.method_not_allowed(request)


# API danh sách sản phẩm (không có images)
class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# API chi tiết sản phẩm (có images)
class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

# API danh sách danh mục
class CategoryListView(CustomAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
