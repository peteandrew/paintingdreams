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
SECRET_KEY = '$2lhfqgr+dw-5+)r!j9t68a-9o55-3xo+^n_0f(43f+-ki*4hj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

ADMINS = [('Admin1', 'admin1@admin.com')]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'mainapp',
    'paypal.standard.ipn',
    'cardsave',
    'django_countries',
    'wholesale',
    'rest_framework',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mainapp.middleware.XForwardedForMiddleware'
)

BASE_URL = 'http://localhost'

ROOT_URLCONF = 'paintingdreams.urls'

WSGI_APPLICATION = 'paintingdreams.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdatabase',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django_debug.log',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Set session time to 1 day
SESSION_COOKIE_AGE = 86400

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'

DEFAULT_FROM_EMAIL = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

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
                'mainapp.context_processors.basket',
                'mainapp.context_processors.holiday_messages',
            ]
        }
    }
]

IMAGE_SIZES = {
    'thumbnail': {
        'path': 'thumbnail',
        'longest_side': 150,
        'watermark': False
    },
    'standard': {
        'path': 'standard',
        'longest_side': 500,
        'watermark': True,
        'watermark_base_size': 40
    },
    'standard-no-watermark': {
        'path': 'standard-no-watermark',
        'longest_side': 500,
        'watermark': False,
    },
    'enlargement': {
        'path': 'enlargement',
        'longest_side': 800,
        'watermark': True,
        'watermark_base_size': 60
    },
    'enlargement-no-watermark': {
        'path': 'enlargement-no-watermark',
        'longest_side': 800,
        'watermark': False,
    },
    'extra-large-no-watermark': {
        'path': 'extra-large-no-watermark',
        'longest_side': 1500,
        'watermark': False,
    },
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

ORDERS_ADMIN_EMAILS = ['orders@example.com']
ORDERS_FROM_EMAIL = 'admin@example.com'

WHOLESALE_ADMIN_EMAILS = ['orders@example.com']

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
       'rest_framework.parsers.JSONParser',
    )
}

GOOGLE_RECAPTCHA_SECRET_KEY = ''

MAILCHIMP_APIKEY = ''
