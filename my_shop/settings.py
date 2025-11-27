import os
import logging
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta, datetime

load_dotenv()


### SETTING JSON WEB TOKEN ###
SIMPLE_JWT = {
    # Thời gian sống của Access Token
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),

    # Thời gian sống của Refresh Token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), 

    # Khi người dùng dùng refresh token để xin access token mới, 
    # hệ thống sẽ tạo luôn một refresh token mới, thay thế cái cũ.
    'ROTATE_REFRESH_TOKENS': True, 

    # Khi refresh token bị thay thế (do ROTATE_REFRESH_TOKENS=True), 
    # token cũ sẽ bị đưa vào danh sách đen (blacklist).
    # Tránh kẻ xấu dùng lại token cũ để xin access token mới.
    'BLACKLIST_AFTER_ROTATION': True,

    # Có cập nhật thời gian đăng nhập cuối cùng của user hay không
    'UPDATE_LAST_LOGIN': False, 

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv("JWT_SECRET_KEY"),
}


# Cấu hình email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

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

    # Thêm Middleware giới hạn request toàn hệ thống    
    "my_shop.middlewares.rate_limit_middleware.GlobalRateLimitMiddleware",
    
    "my_shop.middlewares.logging_middleware.AdvancedSecurityLoggingMiddleware",
    
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

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

    "site_logo": "/home/images/site_logo.png",
    
    "login_logo": "/home/images/site_logo.png",
    
    "show_ui_builder": False,

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


AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 0.01
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = "home/lockout.html"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ) + ( 
        ('rest_framework.renderers.BrowsableAPIRenderer',) if DEBUG else ()
    ),
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "1",
    }
}

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
        }

        # message gốc (nếu không ghi gì thì message = "request log")
        if record.msg:
            log_data["message"] = record.getMessage()

        # merge extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data, ensure_ascii=False)



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": JsonFormatter},
    },
    "filters": {
        "ignore_favicon": {
            "()": "utils.logging_handlers.IgnoreFaviconFilter",
        },
    },
    "handlers": {
        "daily_file": {
            "level": "INFO",
            "class": "utils.logging_handlers.DailyLogFileHandler",
            "dirname": os.path.join(BASE_DIR, "logs"),
            "prefix": "django-logs",
            "formatter": "json",
            "filters": ["ignore_favicon"],
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["daily_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
