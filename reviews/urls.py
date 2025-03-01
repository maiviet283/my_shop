from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='list'),
    path('<int:pk>/', views.ReviewProductDetailView.as_view(), name='detail'),
]