"""
Django settings for paintingdreams project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['srvr.paintingdreams.co.uk']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'carton',
    'crispy_forms',
    'mainapp',
    'paypal.standard.ipn',
    'cardsave',
    'django_countries',
    'wholesale',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mainapp.middleware.XForwardedForMiddleware'
)

BASE_URL = 'https://www.paintingdreams.co.uk'

ROOT_URLCONF = 'paintingdreams.urls'

WSGI_APPLICATION = 'paintingdreams.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/gunicorn/django_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

import logging.config
logging.config.dictConfig(LOGGING)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = ''
#EMAIL_PORT = 465
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
##EMAIL_USE_TLS
#EMAIL_USE_SSL = True
#EMAIL_TIMEOUT = 5
##EMAIL_SSL_KEYFILE
##EMAIL_SSL_CERTFILE


DEFAULT_FROM_EMAIL = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processors.basket'
            ]
        }
    }
]

IMAGE_SIZES = {
    'standard': {
        'path': 'standard',
        'longest_side': 500,
        'watermark': True,
        'watermark_base_size': 40
    },
    'enlargement': {
        'path': 'enlargement',
        'longest_side': 800,
        'watermark': True,
        'watermark_base_size': 60
    },
    'thumbnail': {
        'path': 'thumbnail',
        'longest_side': 150,
        'watermark': False
    }
}

CART_PRODUCT_MODEL = 'mainapp.models.Product'

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = ''
PAYPAL_CURRENCY_CODE = 'GBP'
PAYPAL_IMAGE = 'https://www.paypalobjects.com/en_US/i/btn/x-click-but6.gif'
PAYPAL_SANDBOX_IMAGE = 'https://www.paypalobjects.com/en_US/i/btn/x-click-but6.gif'

CARDSAVE_MERCHANT_ID = ''
CARDSAVE_PRESHARED_KEY = ''
CARDSAVE_PASSWORD = ''
CARDSAVE_CURRENCY_CODE = 826 # ISO 4217 GBP
CARDSAVE_REQUEST_URL = 'https://mms.cardsaveonlinepayments.com/Pages/PublicPages/PaymentForm.aspx'
CARDSAVE_ORDER_MODEL = 'mainapp.models.OrderTransaction'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

COUNTRIES_FIRST = [
    'GB',
]

COUNTRIES_OVERRIDE = {
    'GB': 'United Kingdom'
}

ORDERS_ADMIN_EMAIL = ''
ORDERS_FROM_EMAIL = ''

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
       'rest_framework.parsers.JSONParser',
    )
}
