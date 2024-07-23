"""
Settings module for the Django project.

This file contains the default configuration for the Django application, including settings
for installed applications, middleware, templates, database configuration, password validation,
internationalization, static files, and more. It also includes configurations for third-party 
applications like Django REST framework, JWT authentication, and email backend settings.
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sv8hm9fmt3$$_pdjz7xl3)dclejl(g358sl7o+jk-0f_!r&my+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


import os

# Other settings...

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Update ALLOWED_HOSTS with the domains you want to allow
ALLOWED_HOSTS = ['*',"*"]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://localhost:8000',
    'http://127.0.0.1:8000',
    'https://127.0.0.1:8000'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files handling
    'rest_framework',  # Django REST framework
    'corsheaders',  # CORS headers handling
    'django_filters',  # Filtering for Django REST framework
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklist
    'assets',  # Custom application for managing assets
    'django_rest_passwordreset',  # Password reset functionality
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session middleware
    'django.middleware.common.CommonMiddleware',  # Common middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection middleware
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Directories to search for templates
        'APP_DIRS': True,  # Enable template loading from application directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Authentication context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite database engine
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file path
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Similarity validator
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # Minimum length validator
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # Common password validator
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # Numeric password validator
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'  # Language code
TIME_ZONE = 'UTC'  # Time zone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support

# Static files (CSS, JavaScript, Images) settings
STATIC_URL = 'static/'  # URL to access static files

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default primary key field type

# Custom user model
AUTH_USER_MODEL = 'assets.CustomUser'  # Custom user model

# Configuring CORS headers to restrict host access
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://localhost:8000",
    # "http://95cc-197-237-236-78.ngrok-free.app",  # Add your domain here
]

# JWT settings configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT authentication class
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token lifetime
    'ROTATE_REFRESH_TOKENS': False,  # Rotate refresh tokens setting
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist after rotation setting
    'UPDATE_LAST_LOGIN': False,  # Update last login setting
    'ALGORITHM': 'HS256',  # Algorithm for signing tokens
    'SIGNING_KEY': SECRET_KEY,  # Signing key for tokens
    'VERIFYING_KEY': None,  # Verifying key for tokens
    'AUDIENCE': None,  # Audience for tokens
    'ISSUER': None,  # Issuer for tokens
    'JSON_ENCODER': None,  # JSON encoder for tokens
    'JWK_URL': None,  # JWK URL for tokens
    'LEEWAY': 0,  # Leeway for token expiration
    'AUTH_HEADER_TYPES': ('Bearer',),  # Auth header types
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # Auth header name
    'USER_ID_FIELD': 'id',  # User ID field
    'USER_ID_CLAIM': 'user_id',  # User ID claim
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',  # User authentication rule
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # Auth token classes
    'TOKEN_TYPE_CLAIM': 'token_type',  # Token type claim
    'JTI_CLAIM': 'jti',  # JTI claim
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # Sliding token refresh expiration claim
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=120),  # Sliding token lifetime
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Sliding token refresh lifetime
}

# Email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Email backend
EMAIL_HOST = 'smtp.gmail.com'  # Email host
EMAIL_PORT = 587  # Email port
EMAIL_USE_TLS = True  # Use TLS for email
EMAIL_HOST_USER = 'developerantony98@gmail.com'  # Email host user
EMAIL_HOST_PASSWORD = 'ejid tsyb acow emcs'  # Email host password
DEFAULT_FROM_EMAIL = 'noreply@gmail.com'  # Default from email

# Configuring send email templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Directories to search for templates
        'APP_DIRS': True,  # Enable template loading from application directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Authentication context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor
            ],
        },
    },
]
