from django.urls import path
from . import views, views_error

app_name = 'customers'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.UpdatePasswordView.as_view(), name='change-password'),

    # Lỗ Hổng SQL Injection
    path('login-sql/', views_error.LoginSQLiDemoView.as_view(), name='login-error'),
]
