from .models import CustomerUser
from .serializers import CustomerUserSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Xử lý đăng ký tài khoản"""
        serializer = CustomerUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Đăng ký tài khoản thành công!",
                "data": {"username": serializer.data.get("username")},
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        """Xử lý ngoại lệ cho phương thức không được phép"""
        if isinstance(exc, Exception) and self.request.method != 'POST':
            return Response({
                "error": "Phương thức không được phép!",
                "suggestion": "Vui lòng sử dụng phương thức POST."
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().handle_exception(exc)
