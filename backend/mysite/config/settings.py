"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import pymysql
import datetime
pymysql.install_as_MySQLdb()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ROOT_DIR = os.path.dirname(BASE_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'config', 'static')
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w=8akg)9oz+fc%chr39z5zalhva&8kznpd0jn_$5ba5v7i!#)k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

<<<<<<< HEAD
# ALLOWED_HOSTS = ["125.6.40.68",]
ALLOWED_HOSTS = ['*']
=======
ALLOWED_HOSTS = ["125.6.40.68", "59mins.net", "125.6.39.225", "sublog.linl", "http://sublog.linl", "http://125.6.39.225:3000/"]
# ALLOWED_HOSTS = ['*']
>>>>>>> b64a49025 (22.03.10 | schedule add & db password modify)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # 추가
    'corsheaders',  # 추가
    'drf_yasg',  # 추가
    'rest_framework.authtoken',
    'pybo',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 로그인
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

# 로그인
JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',  # 암호화 알고리즘
    'JWT_ALLOW_REFRESH': False,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 추가
    'django.middleware.common.CommonMiddleware',  # 추가
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = ['http://localhost:3000']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bside',
        'USER': 'root',
        'PASSWORD': '',  # 대영
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# STATIC_URL = '/static/'
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     STATIC_DIR,
# ]
# STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')


AUTH_USER_MODEL = 'pybo.User'
