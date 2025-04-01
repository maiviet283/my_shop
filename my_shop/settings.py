"""
Django settings for my_shop project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/

"""

from pathlib import Path
import os
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Thời gian sống của Access Token
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=20),     # Thời gian sống của Refresh Token
    'ROTATE_REFRESH_TOKENS': True,                 # Có tự động làm mới Refresh Token khi làm mới Access Token hay không
    'BLACKLIST_AFTER_ROTATION': True,               # Có vô hiệu hóa Refresh Token sau khi nó được làm mới hay không
    'UPDATE_LAST_LOGIN': False,                     # Có cập nhật thời gian đăng nhập cuối cùng của user hay không
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g_pb0squy63k+&7hnnp$rn5vpwygw%l-k&gm%vgky#fn)iz^g%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

HANDLER_404 = 'home.views.custom_404_view'
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customers',
    'products',
    'reviews',
    'orders',
    'payments',
    'home',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    "axes",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "axes.middleware.AxesMiddleware",

    # Whitenoise để xử lý file tĩnh.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # Thêm Middleware giới hạn request toàn hệ thống
    "my_shop.middlewares.rate_limit_middleware.GlobalRateLimitMiddleware",

]


if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "https://your-frontend.com",
        "https://your-other-domain.com",
    ]


ROOT_URLCONF = 'my_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = '/static/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEDITOR_UPLOAD_PATH = 'ckeditor/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_icon": "/home/images/favicon.png",
    "site_title": "Hệ Thống Quản Lý Cửa Hàng",
    "site_header": "Trang Admin",
    "site_brand": "Cửa Hàng",
    "welcome_sign": "Chào mừng bạn đến với hệ thống quản lý",
    "copyright": "© 2025 Cửa Hàng",
    "topmenu_links": [
        {"name": "Trang Chủ", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
    ],

    # Logo trên sidebar
    "site_logo": "/home/images/site_logo.png",
    
    # Logo trên trang đăng nhập
    "login_logo": "/home/images/logo.png",
    
    "show_ui_builder": False,  # Bật tính năng kéo thả UI

    "order_with_respect_to": [
        "auth",
        "customers",
        "products",
        "orders",
        "payments",
        "reviews",
        "axes",
        "home",
        "rest_framework_simplejwt.token_blacklist",
    ],
}


# Chặn tấn Công Brute-Force
AXES_FAILURE_LIMIT = 5  # Chặn sau 5 lần đăng nhập sai
AXES_COOLOFF_TIME = 0.01  # Chặn trong 1 giờ (đơn vị: giờ)
AXES_RESET_ON_SUCCESS = True  # Reset bộ đếm khi đăng nhập đúng
AXES_LOCKOUT_TEMPLATE = "home/lockout.html"  # Trang bị khóa đăng nhập

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",  # Django Axes - Chống brute-force
    "django.contrib.auth.backends.ModelBackend",  # Mặc định của Django
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',  # Luôn trả JSON
    ) + ( 
        ('rest_framework.renderers.BrowsableAPIRenderer',) if DEBUG else ()  # Chỉ bật khi DEBUG=True
    ),
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "SERIALIZER": "django_redis.serializers.json.JSONSerializer",  # Sử dụng JSON
#         },
#     }
# }

CACHES = {
    "default": {  # Định nghĩa cache mặc định
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",  # Dùng bộ nhớ RAM cục bộ
        "LOCATION": "1",  # Mã định danh (ID) của cache, có thể đặt tên tùy ý
    }
}
