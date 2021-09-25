

from datetime import timedelta
from pathlib import Path
import os
import django_heroku


import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = 'django-insecure-6^4ca9$ml4l1c#36gkc*z3#8(h_(9efte_*(03byw4real%7rl'

# DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["198.199.73.102","localhost", "127.0.0.1", 'api.rennintech.com', "nsrohub.herokuapp.com", "143.244.153.209"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'rest_framework',
    'mp_operations',
    'constituent_operations',
    'general',
    'corsheaders',
    'routing',
    'superadmin_operations',
    'chatsystem',
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
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'nsromahub_project_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'nsromahub_project_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# if DEBUG:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'sapadb',
#             'USER': 'sapauserdb',
#             'PASSWORD': 'P@ssw0rd1998',
#             'HOST': 'localhost',
#             'PORT': '',
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


DATE_INPUT_FORMATS = ['%d-%m-%Y']

AUTH_USER_MODEL = 'users.CustomUser'



JWT_AUTH = {
  'JWT_ENCODE_HANDLER':
  'rest_framework_jwt.utils.jwt_encode_handler',
  'JWT_DECODE_HANDLER':
  'rest_framework_jwt.utils.jwt_decode_handler',
  'JWT_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_payload_handler',
  'JWT_PAYLOAD_GET_USER_ID_HANDLER':
  'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
  'JWT_RESPONSE_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_response_payload_handler',
 
  'JWT_SECRET_KEY': SECRET_KEY,
  'JWT_GET_USER_SECRET_KEY': None,
  'JWT_PUBLIC_KEY': None,
  'JWT_PRIVATE_KEY': None,
  'JWT_ALGORITHM': 'HS256',
  'JWT_VERIFY': True,
  'JWT_VERIFY_EXPIRATION': False,
  'JWT_LEEWAY': 0,
  'JWT_EXPIRATION_DELTA': timedelta(days=365),
  'JWT_AUDIENCE': None,
  'JWT_ISSUER': None,
  'JWT_ALLOW_REFRESH': False,
  'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=365),
  'JWT_AUTH_HEADER_PREFIX': 'Bearer',
  'JWT_AUTH_COOKIE': None,
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.IsAuthenticated',
         'rest_framework.permissions.IsAdminUser',
         ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    
    # 'DEFAULT_PERMISSION_CLASSES': [
    # 'rest_framework.permissions.IsAuthenticated',
    # ],

    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


SILENCED_SYSTEM_CHECKS = ['auth.E003', 'auth.W004']

google_pass = env('google_pass')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rennintech@gmail.com'
EMAIL_HOST_PASSWORD = google_pass
ACCOUNT_EMAIL_VERIFICATION = 'none'



CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    '*',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    "*"
]


CORS_ALLOWED_ORIGINS = ["https://*", "http://*"]


aws_access = env('aws_access')
aws_secret = env('aws_secret')


# AWS_ACCESS_KEY_ID = aws_access
# AWS_SECRET_ACCESS_KEY = aws_secret
# AWS_STORAGE_BUCKET_NAME = 'sapa-bucket'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'





django_heroku.settings(locals())


# STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# SESSION_COOKIE_SECURE = True
