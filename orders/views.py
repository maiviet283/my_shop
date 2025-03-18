from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from products.models import Product
from customers.views import CustomJWTAuthentication
from .serializers import CartSerializer


# API để xem thông tin giỏ hàng của người dùng.
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = request.user
        # Kiểm tra xem giỏ hàng có tồn tại không
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            return Response({"message": "Giỏ hàng trống."}, status=status.HTTP_200_OK)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Thêm sản phẩm vào giỏ hàng và +1 sản phẩm khi đã ở trong giỏ hàng
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, id):
        user = request.user
        quantity = int(request.data.get("quantity", 1))
        product = get_object_or_404(Product, id=id)

        if product.stock < quantity:
            return Response({
                "message": "Sản phẩm không đủ số lượng trong kho."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Lấy hoặc tạo giỏ hàng của người dùng
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            if cart_item.quantity + quantity > product.stock:
                return Response({
                    "message": "Sản phẩm không đủ số lượng trong kho."
                }, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response({
            "message": "Sản phẩm đã được thêm vào giỏ hàng."
        }, status=status.HTTP_200_OK)


# Xóa số lượng đi 1 khi người dùng muốn giảm
class DecreaseCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, id):
        user = request.user
        # Kiểm tra sản phẩm có tồn tại trong giỏ hàng không
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=id)

        if cart_item.quantity > 0:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            return Response({
                    "message": "Không thể giảm số lượng xuống dưới 0."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
                "message": "Đã giảm số lượng sản phẩm."
            }, status=status.HTTP_200_OK)


# Xóa sản phẩm khỏi giỏ hàng
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def delete(self, request, id):
        user = request.user
        # Kiểm tra giỏ hàng và sản phẩm trong giỏ hàng
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=id)
        # Xóa sản phẩm khỏi giỏ hàng
        cart_item.delete()
        return Response({
                "message": "Sản phẩm đã được xóa khỏi giỏ hàng."
            }, status=status.HTTP_200_OK)
