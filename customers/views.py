from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from .models import CustomerUser
from .serializers import *
from orders.models import Cart


# Tạo Tài Khoản Khách Hàng + Tạo Giỏ Hàng Tương Ứng
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Xử lý đăng ký tài khoản (Chỉ nhận username, email, password)"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Cart.objects.create(user=user) # Tạo giỏ hàng cho người dùng mới
            return Response({
                "message": "Đăng ký tài khoản thành công!",
                "data": {"username": serializer.data.get("username")},
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Đăng Nhập Tài Khoản Khách Hàng
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = CustomerUser.objects.get(username=username)
            
            if check_password(password,user.password):
                refresh = RefreshToken()
                refresh["id"] = user.pk
                refresh["username"] = user.username
                access = refresh.access_token

                return Response({
                    "message": "Đăng nhập thành công!",
                    "tokens": {
                        "access": str(access),
                        "refresh": str(refresh)
                    }
                }, status=status.HTTP_200_OK)
            
            else: 
                return Response({
                    'error':'Tên đăng nhập hoặc mật khẩu không đúng'
                },status=status.HTTP_400_BAD_REQUEST)
            
        except CustomerUser.DoesNotExist:
            return Response({
                'error':'Tên đăng nhập hoặc mật khẩu không đúng'
            }, status=status.HTTP_401_UNAUTHORIZED)
        

# (Chung) Lấy Thông Tin
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('id')
            if not user_id:
                raise InvalidToken("Token Thông Báo Không có ID trên")
            
            user = CustomerUser.objects.get(id=user_id)
            return user
        except CustomerUser.DoesNotExist:
            raise InvalidToken("Khách Hàng Này Không Tồn Tại")


# Lấy Thông Tin Tài Khoản Khách Hàng
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        serializer = CustomerUserSerializer(request.user)
        return Response({
            "message": "Lấy Thông Tin của Quý Khách Thành Công",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

# Cập Nhật Thông Tin Tài Khoản Khách Hàng
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def put(self, request):
        serializer = UpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Cập Nhật Thông Tin Tài Khoản Thành Công",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Cập Nhật Mật Khẩu Tài Khoản Khách Hàng
class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update_password()  # Cập nhật mật khẩu
            return Response({"message": "Mật khẩu đã được thay đổi thành công."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Refresh Token
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Cần có Mã Refresh Token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = token.access_token

            return Response({
                'access': str(new_access_token),
                'refresh': str(token),
            })
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

# Đăng Xuất Tài Khoản Khách Hàng
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error': 'Cần có Mã Refresh Token'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Đăng xuất thành công. Refresh token đã bị vô hiệu hóa.'
            }, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({
                'error': 'Refresh token không hợp lệ hoặc đã hết hạn.',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)