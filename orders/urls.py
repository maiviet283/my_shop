from django.urls import path
from . import views, order_views

app_name = 'orders'

urlpatterns = [
    # Cart
    path('add-to-cart/<int:id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('decrease-cart-item/<int:id>/', views.DecreaseCartItemView.as_view(), name='decrease_cart_item'),
    path('remove-from-cart/<int:id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/', views.CartDetailView.as_view(), name='cart-detail'),
    path('count-in-cart', views.CountProductInCart.as_view(),name='count-in-cart'),

    # Order
    path('create-order/', order_views.CreateOrderView.as_view(), name='create_order'),
    
]
