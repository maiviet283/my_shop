from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.static import serve

# Create your views here.
def index(request):
    return render(request, 'home/welcome.html')

def swagger(request):
    return render(request, 'home/swagger.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def serve_media(request, path):
    """
    Chỉ phục vụ file trong `media/` nếu DEBUG=True
    """
    if settings.DEBUG:
        return serve(request, path, document_root=settings.MEDIA_ROOT)
    return HttpResponseForbidden("Access Denied")