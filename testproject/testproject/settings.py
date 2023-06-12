"""
Django settings for testproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os

try:
    import guardian
    has_guardian = True
except ImportError:
    has_guardian = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9vg3q-kbo(p^zpom4!*o8*%tfu-14o=3++txo+sxwto)2@=qd='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',

    # Uncomment for testing templates, and after a `pip install django-bootstrap3`
    'bootstrap3',

    # App test
    'groups_manager',
    'testproject',

    # mptt provides the templates for rendering trees in admin
    'mptt',
)

if has_guardian:
    INSTALLED_APPS += ('guardian',)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MIDDLEWARE_CLASSES = MIDDLEWARE

# django-guardian required settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'testproject.urls'

WSGI_APPLICATION = 'testproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SESSION_COOKIE_NAME = "testproject"
LOGIN_URL = '/admin/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 'django.contrib.auth.context_processors.auth',
                 'django.contrib.messages.context_processors.messages',
                 'django.template.context_processors.request',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Uncomment to test application settings

"""
GROUPS_MANAGER = {
    'AUTH_MODELS_SYNC': True,
    'AUTH_MODELS_GET_OR_CREATE': False,
    'GROUP_NAME_PREFIX': '',
    'GROUP_NAME_SUFFIX': '',
    'USER_USERNAME_PREFIX': '',
    'USER_USERNAME_SUFFIX': '',
    'PERMISSIONS': {
        'owner': ['view', 'change', 'delete'],
        'group': ['view', 'change'],
        'groups_upstream': ['view'],
        'groups_downstream': [],
        'groups_siblings': ['view'],
    },
}
"""

# Uncomment to test slugify function with awesome-slugify

"""
from slugify import slugify
GROUPS_MANAGER = {
    'SLUGIFY_FUNCTION': lambda s: slugify(s, to_lower=True),
    'SLUGIFY_USERNAME_FUNCTION': lambda s: slugify(s, to_lower=True, separator="_")
}
"""

# Setting for mptt-tree in admin UI (default: 20)
MPTT_ADMIN_LEVEL_INDENT = 25
