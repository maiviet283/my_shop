from django.http import JsonResponse

class FileSizeLimitMiddleware:
    """
    Không được sử dụng : Đã được làm trong Serializer rồi
    Middleware giới hạn kích thước file tải lên (1MB).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.max_upload_size = 500 * 1024  # 500 KB

    def __call__(self, request):
        if request.method in ["PUT"] and request.FILES:
            print("vcl")
            for file in request.FILES.values():
                if file.size > self.max_upload_size:
                    return JsonResponse(
                        {"error": "File tải lên quá lớn! Giới hạn tối đa là 500 KB."},
                        status=400
                    )
        return self.get_response(request)
