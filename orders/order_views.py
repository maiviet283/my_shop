from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, Order, OrderItem
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

        # Kiểm tra địa chỉ giao hàng của người dùng
        if not user.address or user.address.strip() == "":
            return Response({"error": "Vui lòng cập nhật địa chỉ giao hàng trước khi đặt hàng."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra số lượng sản phẩm trong kho trước khi đặt hàng
        for cart_item in cart.items.all():
            if cart_item.product.stock < cart_item.quantity:
                return Response({
                    "error": f"Sản phẩm '{cart_item.product.name}' không đủ hàng trong kho."
                }, status=status.HTTP_400_BAD_REQUEST)

        # Tạo đơn hàng
        order = Order.objects.create(user=user, total_price=cart.total_price())

        # Chuyển CartItem thành OrderItem và giảm số lượng trong kho
        for cart_item in cart.items.all():
            product = cart_item.product
            OrderItem.objects.create(order=order, product=product, quantity=cart_item.quantity)
            product.stock -= cart_item.quantity
            product.save()

        # Xóa giỏ hàng sau khi đặt hàng
        cart.clear_cart()

        return Response({"message": "Đơn hàng đã được tạo.", "order_id": order.id}, status=status.HTTP_201_CREATED)
