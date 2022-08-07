import os
from importlib.resources import path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-d3d2*@8c7yy(_2ml%l9hr$kctf6apk04!in-vrq3*0)q1jza0u'

DEBUG = False

ALLOWED_HOSTS = ['amestock-ecomerce.herokuapp.com', '127.0.0.1', 'localhost']
# ALLOWED_HOST = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paypal.standard.ipn',
    'analytics',
    'emails',
    'products',
    'profiles',
    'accounts',
    'orders',
    'sellers',
    'tags',
    'watermarker',
    # "anymail",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'Ecodig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'Ecodig.wsgi.application'
AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ANYMAIL = {
#     "MAILGUN_API_KEY": "949344ed012e8b4ea353523f09e57669-835621cf-c4fbca06",
#     "SEND_DEFAULTS": {
#         "tags": ["Meshutter"]
#     },
#     "IGNORE_RECIPIENT_STATUS": True,
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/




STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATIC_ROOT = Path.joinpath(BASE_DIR, '/static/')
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR/ "mediaProt"/ "media"

PROTECTED_MEDIA = BASE_DIR/ "mediaProt"/ "protected"

if DEBUG:
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    PROTECTED_MEDIA.mkdir(parents=True, exist_ok=True)
    


PAYPAL_RECEIVER_EMAIL = 'sb-czqyo16979431@business.example.com'

PAYPAL_TEST = True

WATERMARKING_QUALITY = 85
WATERMARK_OBSCURE_ORIGINAL = False

# WATERMARK_RANDOM_POSITION_ONCE = False
# WATERMARK_OBSCURE_ORIGINAL = False
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field


# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'amecomglobalenterp@gmail.com'
# EMAIL_HOST_PASSWORD= 'nsxqgbgysgpradet'
# EMAIL_USE_TSL= True
# EMAIL_USE_SSL= False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '470baf9f7e5d6b'
EMAIL_HOST_PASSWORD = '306c6b7e130846'
EMAIL_PORT = '2525'


