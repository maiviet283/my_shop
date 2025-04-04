from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# Đăng Nhập Tài Khoản Khách Hàng (CÓ LỖ HỔNG SQL INJECTION)
class LoginSQLiDemoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        raw_query = f"""
            SELECT id, username FROM customers_customeruser 
            WHERE username = '{username}' AND password = '{password}'
        """

        # In ra để thấy query sau khi bị inject
        print("⚠️ SQL QUERY:", raw_query)  

        from django.db import connection
        with connection.cursor() as cursor:
            try:
                cursor.execute(raw_query)
                user = cursor.fetchone()
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        if user:
            user_id, username = user
            refresh = RefreshToken()
            refresh["id"] = user_id
            refresh["username"] = username
            access = refresh.access_token

            return Response({
                "message": "Đăng nhập thành công!",
                "query_used": raw_query,
                "tokens": {
                    "access": str(access),
                    "refresh": str(refresh)
                }
            })

        return Response({"error": "Đăng nhập thất bại!", "query_used": raw_query}, status=400)