"""
Django settings for mywebsite project.
"""

from pathlib import Path
import os

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SECURITY SETTINGS
# ==========================================

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-32h4uj%e&)x=u#j(j^d_o^#*m^8)@pt!765jds=783n43a67z!'
)

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# ==========================================
# INSTALLED APPLICATIONS
# ==========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Mini Product Catalogue application
    'catalogue',
]


# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================
# URL CONFIGURATION
# ==========================================

ROOT_URLCONF = 'mywebsite.urls'


# ==========================================
# TEMPLATE CONFIGURATION
# ==========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================================
# WSGI CONFIGURATION
# ==========================================

WSGI_APPLICATION = 'mywebsite.wsgi.application'


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# PASSWORD VALIDATION
# ==========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# ==========================================
# LANGUAGE AND TIME
# ==========================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# ==========================================
# STATIC FILES
# ==========================================

STATIC_URL = '/static/'


# ==========================================
# MEDIA FILES
# ==========================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# EMAIL CONFIGURATION
# PASSWORD RESET TESTING
# ==========================================

EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
)

DEFAULT_FROM_EMAIL = 'admin@example.com'


# ==========================================
# LOGIN AND LOGOUT SETTINGS
# ==========================================

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# ==========================================
# RAZORPAY PAYMENT CONFIGURATION
# ==========================================

# Store your Razorpay credentials in environment variables.
# Do not put your actual secret key in HTML or JavaScript.

RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', '')

RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '')


# ==========================================
# DEFAULT PRIMARY KEY FIELD
# ==========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
