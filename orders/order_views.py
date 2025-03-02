from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from customers.views import CustomJWTAuthentication


# Tạo Đơn Hàng Từ Giỏ Hàng
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)

        if not cart.items.exists():
            return Response({"error": "Giỏ hàng trống."}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo đơn hàng
        order = Order.objects.create(user=user, total_price=cart.total_price())

        # Chuyển CartItem thành OrderItem
        for cart_item in cart.items.all():
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

        # Xóa giỏ hàng sau khi đặt hàng
        cart.clear_cart()

        return Response({"message": "Đơn hàng đã được tạo.", "order_id": order.id}, status=status.HTTP_201_CREATED)
