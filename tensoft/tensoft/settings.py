"""
Django settings for tensoft project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'teu&hb6m$o64%n!5dn5*fhcyfot=4b5046gloytphwtchawhe%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '.localhost']


# Application definition
SHARED_APPS = (
    #APP DE LA HERRAMIENTA DJANGO-TENANTS
    'django_tenants',
    #APP QUE CONTIENE EL MANEJO DE TENANTS
    'inmobiliaria_tenant',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'bootstrap3',
    'captcha',
    'parreporter_tool',
)

TENANT_APPS = (    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'inmuebles',

    #'mensajes',
)

INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))

TENANT_MODEL = "inmobiliaria_tenant.Inmobiliaria"  # app.Model
TENANT_DOMAIN_MODEL = "inmobiliaria_tenant.Domain"

GOOGLE_RECAPTCHA_SECRET_KEY = '6LcdV1MUAAAAAHM8NjfYANxwvPYotHr_zz-wlmDi'
NOCAPTCHA = True

MIDDLEWARE_CLASSES = [
    'django_tenants.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tensoft.tenant_urls'
PUBLIC_SCHEMA_URLCONF = 'tensoft.public_urls'

PUBLIC_SCHEMA_NAME = 'public'

LOGIN_URL = '/cuenta/login/'
LOGOUT_REDIRECT_URL = '/cuenta/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'tensoft.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'inmobiliarias_tensoft',
        'USER': 'univalle',
        'PASSWORD': 'univalle',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'soporte.tensoft@gmail.com'
EMAIL_HOST_PASSWORD = 'univalle'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Soporte TenSoft <noreply@TenSoft.com>'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static_collected')


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/'
