from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),   # Lấy danh sách sản phẩm
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),  # Lấy chi tiết sản phẩm
    path('category', CategoryListView.as_view(), name='category-list'),   # Lấy danh sách danh mục
]
