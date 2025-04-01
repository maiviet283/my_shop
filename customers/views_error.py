from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Đăng Nhập Tài Khoản Khách Hàng (CÓ LỖ HỔNG SQL INJECTION)
class LoginErrorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # ❌ Dễ bị SQL Injection vì nối trực tiếp input vào query
        query = f"SELECT id, username FROM customers_customeruser WHERE username = '{username}' AND password = '{password}'"

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()  # Nếu có user, fetchone() sẽ trả về tuple (id, username)

        if user:
            user_id, username = user

            # ✅ Vẫn tạo token để so sánh với phiên bản an toàn
            refresh = RefreshToken()
            refresh["id"] = user_id
            refresh["username"] = username
            access = refresh.access_token

            return Response({
                "message": "Đăng nhập thành công! (CÓ LỖ HỔNG SQL INJECTION)",
                "tokens": {
                    "access": str(access),
                    "refresh": str(refresh)
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Tên đăng nhập hoặc mật khẩu không đúng"}, status=status.HTTP_400_BAD_REQUEST)
        