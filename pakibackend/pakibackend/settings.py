"""
Django settings for pakibackend project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jjmy43&3_0jssldygo2r_vt_yzmy7jg+ah)68jv+jjl0l$4&#('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# OPEN ID Connect Security Settings
OPEN_ID_CONNECT_SERVER = "https://auth.demo.pragmaticindustries.de/auth/realms/packi"

OIDC_RP_SIGN_ALGO='RS256'
OIDC_OP_JWKS_ENDPOINT = "%s/protocol/openid-connect/certs" % OPEN_ID_CONNECT_SERVER
SESSION_SAVE_EVERY_REQUEST = True
OIDC_RP_CLIENT_ID = "packi"
OIDC_RP_CLIENT_NAME = "packi"
OIDC_RP_NAME = "packi"
OIDC_RP_CLIENT_SECRET = "651bb3dd-ffb6-4ef3-b5ba-151acd73b9e7"
OIDC_DRF_AUTH_BACKEND = 'mozilla_django_oidc.auth.OIDCAuthenticationBackend'
OIDC_OP_AUTHORIZATION_ENDPOINT = "%s/protocol/openid-connect/auth" % OPEN_ID_CONNECT_SERVER
OIDC_OP_TOKEN_ENDPOINT = "%s/protocol/openid-connect/token" % OPEN_ID_CONNECT_SERVER
OIDC_OP_USER_ENDPOINT = "%s/protocol/openid-connect/userinfo" % OPEN_ID_CONNECT_SERVER
OIDC_CREATE_USER = True
OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True
OIDC_OP_LOGOUT_ENDPOINT = "%s/protocol/openid-connect/logout" % OPEN_ID_CONNECT_SERVER
OIDC_OP_LOGIN_ENDPOINT = "https://auth.demo.pragmaticindustries.de/auth"
OIDC_RP_SCOPES = "openid email"
LOGIN_REDIRECT_URL = "https://paki.pragmaticminds.de/login/home"
LOGOUT_REDIRECT_URL = "/"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'paki',
    'mozilla_django_oidc'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

ROOT_URLCONF = 'pakibackend.urls'

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

WSGI_APPLICATION = 'pakibackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
