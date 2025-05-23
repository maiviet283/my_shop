import requests
from django.http import HttpResponse
from customers.views import CustomJWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment

# Hàm Tạo Mã QR
def generate_qr(request, amount=None, note=None):
    bank_code = "VCB"
    account_number = "1015261005"
    qr_url = f"https://img.vietqr.io/image/{bank_code}-{account_number}-qr.png"
    
    params = []
    if amount:
        params.append(f"amount={amount}")
    if note:
        params.append(f"addInfo={note}")
    
    if params:
        qr_url += "?" + "&".join(params)

    response = requests.get(qr_url)
    return HttpResponse(response.content, content_type="image/png")