"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

env = environ.Env(
    # set casting, default value
    # DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENT_FOLDER="documents"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yi(%^bh(5my=92(=qw6pmc_=!v73f1xsx%ga=s!-nvox0dsqzl'
MYMEMORY_KEY = '9d62199240694d4c2176'

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = False
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
ALLOWED_HOSTS = ['*']

DEBUG = True
# ALLOWED_HOSTS = []

INDEX_TM = 'translation_memory'
INDEX_GLOSSARY = 'glossary'
INDEX_CORPUS = 'corpus'


# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',


  'django_elasticsearch_dsl',
  # 'django_elasticsearch_dsl_drf',
  'rest_framework',
  'django.contrib.sites',
  'cat',
  # 'search_indexes',

  'rest_framework.authtoken',
  'drf_yasg',
  'multiselectfield',
  'django_extensions'
]

SITE_ID=1

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',

  'request_logging.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
  # 'default': {
  #     'ENGINE': 'django.db.backends.sqlite3',
  #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'cat',
    'USER': 'postgres',
    'PASSWORD': env('POSTGRES_PASSWORD'),
    # 'PASSWORD': 'postgres@clc',
    'HOST': '172.17.0.1',
    'PORT': '5433',
  }
}

from datetime import timedelta
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=100),
  'ROTATE_REFRESH_TOKENS': False,
  'BLACKLIST_AFTER_ROTATION': True,

  'ALGORITHM': 'HS256',
  'SIGNING_KEY': SECRET_KEY,
  'VERIFYING_KEY': None,
  'AUDIENCE': None,
  'ISSUER': None,

  'AUTH_HEADER_TYPES': ('Bearer',),
  'USER_ID_FIELD': 'id',
  'USER_ID_CLAIM': 'user_id',

  'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
  'TOKEN_TYPE_CLAIM': 'token_type',

  'JTI_CLAIM': 'jti',

  'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
  'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
  'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
VIETNAMESE = 'vi'
ENGLISH = 'en'
LANGUAGE = [
  (ENGLISH, 'English'),
  (VIETNAMESE, 'Vietnamese')
]
ARR_LANGUAGE = [VIETNAMESE, ENGLISH]
TRANSLATION_SERVICE = [
  ('gt', 'Google Translate'),
  ('mm', 'My Memory'),
  ('onmt', 'Open NMT')
]

SIMILARITY_TYPE = [
  ('lev', 'Lexical Similarity: Levenshtein'),
  ('bert', 'Semantic Similarity: BERT Model')
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# https://medium.com/quick-code/token-based-authentication-for-django-rest-framework-44586a9a56fb


REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    # 'rest_framework.authentication.TokenAuthentication',
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
  'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated', ),

  'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

  'DEFAULT_THROTTLE_CLASSES':[
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle'
    ],

  'DEFAULT_THROTTLE_RATES': {
    'anon': '500/minute',
    'user': '3000/minute'
  }
}

ONMT_HOST = '0.0.0.0'
ONMT_PORT = '5000'
ONMT_URL = 'http://' + ONMT_HOST + ':' + ONMT_PORT + '/translator/translate'
ONMT_MODEL_EN_VI = 0
ONMT_MODEL_VI_EN = 1

ELAS_HOST = '172.17.0.1'
ELAS_PORT = '9201'
ELAS_NUM_GLOSSARY_RETURN = '100'
ELAS_NUM_TM_RETURN = '10'
ELAS_NUM_CORPUS_RETURN = '100'

ELASTICSEARCH_DSL = {
  'default': {
    # 'hosts': 'http://localhost:9200'
    'hosts': ELAS_HOST+":"+ELAS_PORT
  },
}

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
    },
  },
  'loggers': {
    'django.request': {
      'handlers': ['console'],
      'level': 'DEBUG',  # change debug level as appropiate
      'propagate': False,
    },
  },
}

FIXTURE_DIRS = (
   '/cat/fixtures/123.json',
)

TEST_FILES_DIR = (
   os.path.join("cat", "tests", "_postman", "data")
)
