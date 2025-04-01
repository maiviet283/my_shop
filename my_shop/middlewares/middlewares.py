from django.shortcuts import render
from django.conf import settings
from django.http import Http404

class Force404Middleware:
    """ Middleware hiển thị trang 404 tùy chỉnh khi DEBUG=True """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Kiểm tra nếu response là lỗi 404
        if response.status_code == 404 and settings.DEBUG:
            return render(request, "404.html", status=404)

        return response
