from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Review
from products.models import Product
from .serializers import ReviewSerializer
from customers.views import CustomJWTAuthentication

class ReviewProductView(APIView):
    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_authenticators(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [CustomJWTAuthentication()]
        return []

    def get(self, request, pk):
        # Kiểm tra xem sản phẩm có tồn tại không
        get_object_or_404(Product, id=pk)
        # Lọc bình luận theo sản phẩm
        reviews = Review.objects.filter(product__id=pk)
        # Nếu không có review nào, trả về thông báo
        if not reviews.exists():
            return Response({
                "message": "Không có bình luận nào cho sản phẩm này."
            },status=status.HTTP_204_NO_CONTENT)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        user = request.user
        rating = request.data.get("rating", 5)
        comment = request.data.get("comment", "")
        
        # Kiểm tra sản phẩm có tồn tại không
        product = get_object_or_404(Product, id=pk)
        
        # Điều chỉnh số sao trong khoảng 1-5
        rating = max(1, min(5, int(rating)))
        
        # Kiểm tra xem user đã đánh giá sản phẩm này chưa
        if Review.objects.filter(product=product, user=user).exists():
            return Response({
                "error": "Bạn đã đánh giá sản phẩm này rồi"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Tạo review mới
        review = Review.objects.create(
            product=product,
            user=user,
            rating=rating,
            comment=comment
        )
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        user = request.user
        review = get_object_or_404(Review, product__id=pk, user=user)
        
        review.rating = max(1, min(5, int(request.data.get("rating", review.rating))))
        review.comment = request.data.get("comment", review.comment)
        review.save()
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        user = request.user
        review = get_object_or_404(Review, product__id=pk, user=user)
        review.delete()
        return Response({
            "message": "Đã xóa bình luận."
        }, status=status.HTTP_204_NO_CONTENT)
