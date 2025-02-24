from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

class CustomAPIView(generics.GenericAPIView):
    """ Chặn tất cả phương thức không hợp lệ """
    
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

class ProductListView(CustomAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(CustomAPIView, generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
