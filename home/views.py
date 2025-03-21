from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home/welcome.html')

def swagger(request):
    return render(request, 'home/swagger.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)