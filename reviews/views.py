from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Review
from .serializers import ReviewSerializer
from products.views import CustomAPIView

# Create your views here.
def index(request):
    return render(request, 'reviews/index.html')

# API danh sách Bình Luận (API này không cần thiết lắm)
class CategoryListView(CustomAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# API chi tiết Bình Luận của Mỗi Sản Phẩm
class CategoryDetailView(CustomAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Lấy id của sản phẩm từ URL
        product_id = self.kwargs.get("pk")
        return Review.objects.filter(product__id=product_id)  # Lọc theo sản phẩm