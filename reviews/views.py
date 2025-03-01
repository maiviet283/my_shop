from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Review
from products.models import Product
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
class ReviewProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        # Kiểm tra xem sản phẩm có tồn tại không
        get_object_or_404(Product, id=pk)
        # Lọc bình luận theo sản phẩm
        reviews = Review.objects.filter(product__id=pk)
        # Nếu không có review nào, trả về thông báo
        if not reviews.exists():
            return Response(
                {"message": "Không có bình luận nào cho sản phẩm này."},
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)