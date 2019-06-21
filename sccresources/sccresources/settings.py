"""
Django settings for sccresources project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import pymysql  # noqa: 402


def get_db_creds():
    """Return database credentials or raise ValueError"""
    try:
        return (os.environ['FG_DB_USER'],
                os.environ['FG_DB_PASSWORD'],
                os.environ['FG_DB_NAME'],
                os.environ.get('FG_DB_CONNECTION_NAME', None))
    except KeyError:
        raise ValueError('Set FG_DB_USER, FG_DB_PASSWORD and FG_DB_NAME to configure database access')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY',
                            's9uupcpes^x2=djgh!q*6w(e5^x^n4v))6@_=7#6r@kag&p5!p')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEPLOYED', 'False') != 'True'

# FIXME: this may slow things down in production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        'sccalendar': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
# See https://docs.djangoproject.com/en/2.1/ref/settings/
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'phonenumber_field',
    'background_task',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sccalendar.apps.SccalendarConfig',
    'addressbook.apps.AddressbookConfig',
    'djrichtextfield',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sccresources.urls'

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
                'sccalendar.context_processor.add_variables_to_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'sccresources.wsgi.application'

if os.environ.get('FG_SQLITE', 'false').lower() == 'true':
    # Use sqlite DB. This is only useful for running test on Travis
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    pymysql.install_as_MySQLdb()
    db_user, db_password, db_name, db_connection_name = get_db_creds()

    if os.getenv('GAE_APPLICATION', None):
        # Running on production App Engine, so connect to Google Cloud SQL using
        # the unix socket at /cloudsql/<your-cloudsql-connection string>
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'HOST': f'/cloudsql/{db_connection_name}',
                'USER': db_user,
                'PASSWORD': db_password,
                'NAME': db_name,
            }
        }
    else:
        # Running locally so connect to either a local MySQL instance or connect to
        # Cloud SQL via the proxy. To start the proxy via command line:
        #
        #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
        #
        # See https://cloud.google.com/sql/docs/mysql-connect-proxy
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'HOST': '127.0.0.1',
                'PORT': '3306',
                'USER': db_user,
                'PASSWORD': db_password,
                'NAME': db_name,
            }
        }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'thefreeguide'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', 'default')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DJRICHTEXTFIELD_CONFIG = {
    'js': ['//tinymce.cachefly.net/4.1/tinymce.min.js'],
    'init_template': 'djrichtextfield/init/tinymce.js',
    'settings': {
        'menubar': False,
        'plugins': 'link image',
        'toolbar': 'bold italic | link image | removeformat',
        'width': 700
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = 'static/'
STATIC_URL = '/static/'
