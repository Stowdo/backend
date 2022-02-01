import os
from pathlib import Path

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=False
ACCOUNT_AUTHENTICATION_METHOD='username'
ACCOUNT_EMAIL_REQUIRED=False
ACCOUNT_EMAIL_VERIFICATION='none'
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
BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('STOWDO_DB_NAME'),
        'USER': os.environ.get('STOWDO_DB_USER'),
        'PASSWORD': os.environ.get('STOWDO_DB_PASSWORD'),
        'HOST': os.environ.get('STOWDO_DB_HOST'),
        'PORT': os.environ.get('STOWDO_DB_PORT')
    },
}
DEBUG = os.environ.get('STOWDO_ENVIRONMENT', 'DEVELOPMENT') == 'DEVELOPMENT'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FILE_STORAGE = 'storage.minio_storage.MinioStorage'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'storage',
]
LANGUAGE_CODE = 'fr-fr'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MINIO_CONFIG = {
    'host': os.environ.get('MINIO_HOST', 'localhost:9000'),
    'access_key': os.environ.get('MINIO_ACCESS_KEY', ''),
    'secret_key': os.environ.get('MINIO_SECRET_KEY', ''),
    'default_bucket': 'default'
}
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}
ROOT_URLCONF = 'stowdo.urls'
SECRET_KEY = os.environ.get('STOWDO_SECRET_KEY')
SITE_ID = 1
STATIC_URL = 'static/'
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
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = 'stowdo.wsgi.application'

# settings depending to DEBUG value
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        'https://stowdo.tk',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
    CSRF_TRUSTED_ORIGINS = [
        'https://stowdo.tk',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
    ALLOWED_HOSTS = [
        '*',
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        'https://stowdo.tk',
    ]
    CSRF_TRUSTED_ORIGINS = [
        'https://stowdo.tk',
    ]
    ALLOWED_HOSTS = [
        'api.stowdo.tk',
    ]