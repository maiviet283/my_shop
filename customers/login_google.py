from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from orders.models import Cart
from .models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify
import requests


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def generate_unique_username(self, base_username):
        username = slugify(base_username)
        counter = 1
        while CustomerUser.objects.filter(username=username).exists():
            username = f"{slugify(base_username)}{counter}"
            counter += 1
        return username

    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Thiếu access_token.'}, status=400)

        try:
            user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(user_info_url, headers=headers)

            if response.status_code != 200:
                return Response({'error': 'Không thể xác thực với Google.'}, status=400)

            user_data = response.json()
            email = user_data.get('email')
            base_username = email.split('@')[0]

            user = CustomerUser.objects.filter(email=email).first()
            if user:
                created = False
            else:
                unique_username = self.generate_unique_username(base_username)
                user = CustomerUser.objects.create(
                    email=email,
                    username=unique_username,
                    is_active=True
                )
                Cart.objects.create(user=user)
                created = True

            refresh = RefreshToken()
            refresh['id'] = user.id
            refresh['username'] = user.username
            access = refresh.access_token

            return Response({
                'message': 'Đăng nhập Google thành công!' + (" (tài khoản mới)" if created else ""),
                'tokens': {
                    'access': str(access),
                    'refresh': str(refresh),
                }
            }, status=200)

        except Exception as e:
            return Response({
                'error': 'Đã xảy ra lỗi trong quá trình đăng nhập.',
                'details': str(e)
            }, status=500)
