"""
Django settings for examples project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# JS:
# Support env variables from .env file if defined
import os
from dotenv import load_dotenv
env_path = load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(env_path)

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-6ibnlx(#h=awfwo-n6pf4w-^7o7%%%4c@pj_w^6$6y4@_a3*%&'
# JS:
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-6ibnlx(#h=awfwo-n6pf4w-^7o7%%%4c@pj_w^6$6y4@_a3*%&')


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# JS:
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'helloworld', # JS
    'modelsapp', # JS
    'bmsapp', # JS
    'studentmgmtsys', # JS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # JS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'examples.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", ], # JS []
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

WSGI_APPLICATION = 'examples.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# JS:
# Update database configuration from $DATABASE_URL environment variable (if defined)
import dj_database_url

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=500,
        conn_health_checks=True,
    )

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# JS:
# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = 'static/'  # or '/static/' ??

# JS: needed?
# other directories for looking for static files
# STATICFILES_DIRS = [BASE_DIR / "static", "/var/www/static/",]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Below by JS =======================================================================

LOGOUT_REDIRECT_URL='/studentmgmtsys' # by default logout redirect to /accounts/logout and show logged-out template
LOGIN_REDIRECT_URL='/studentmgmtsys'# by default login redirect to /accounts/profile and show a custom profile page
# LOGIN_URL='/login/'

MEDIA_ROOT = BASE_DIR / "media"  # path to store media files (under project root)
MEDIA_URL = "/media/"		     # URL to serve media files

# log-out users automatically
# https://stackoverflow.com/questions/31670231/autologout-a-user-after-specific-time-in-django
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # Expire the session when the user closes their browser
SESSION_COOKIE_AGE = 1 * 60 * 60  # 1 hour
# To log-out users automatically after 'X' amount of time has elapsed since they last logged-in
# SESSION_SAVE_EVERY_REQUEST = False  # Only save session when session modified
# To log-out users automatically after 'X' amount of time has elapsed since they were last active
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session whenever user is active


# CSRF_TRUSTED_ORIGINS

# https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
# HTTPS
# CSRF_COOKIE_SECURE = True
# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.

# SESSION_COOKIE_SECURE = True
# Set this to True to avoid transmitting the session cookie over HTTP accidentally.

# Static file serving.
# https://whitenoise.readthedocs.io/en/stable/django.html#add-compression-and-caching-support
# STORAGES = {
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }