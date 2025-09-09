import logging
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

class GlobalRateLimitMiddleware:
    """
    Middleware giới hạn số request toàn hệ thống để chống spam và tấn công DDoS nhẹ.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        if not client_ip:
            return self.get_response(request)

        limit = 50
        timeframe = 5
        block_time = 7

        cache_key = f"rl:{client_ip}"
        block_key = f"blocked:{client_ip}"

        # Kiểm tra IP có đang bị chặn không
        if cache.get(block_key):
            logger.warning(f"IP {client_ip} vẫn đang bị chặn!")
            return self.handle_rate_limit(request)

        request_count = cache.get(cache_key, 0)

        if request_count >= limit:
            logger.warning(f"IP {client_ip} bị chặn do quá nhiều request!")
            cache.set(block_key, 1, timeout=block_time)
            cache.delete(cache_key)
            return self.handle_rate_limit(request)

        # Tăng số lượng request và đặt lại thời gian hết hạn của cache
        cache.set(cache_key, request_count + 1, timeout=timeframe)

        return self.get_response(request)

    def handle_rate_limit(self, request):
        """Xử lý khi bị giới hạn request"""
        error_message = "Bạn đã gửi quá nhiều yêu cầu! Hãy thử lại sau 7 giây."
        if request.headers.get("Accept") == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": error_message}, status=429)
        return render(request, "home/rate_limit.html", {"error_message": error_message}, status=429)

    def get_client_ip(self, request):
        """Lấy địa chỉ IP của client"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
