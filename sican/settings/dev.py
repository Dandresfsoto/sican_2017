from sican.settings.base import *

INSTALLED_APPS += (
    'debug_toolbar',
)


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('SICAN_DB_NAME'),
            'USER': os.getenv('SICAN_DB_USER'),
            'PASSWORD': os.getenv('SICAN_DB_PASSWORD'),
            'HOST': os.getenv('SICAN_DB_HOST'),
            'PORT': os.getenv('SICAN_DB_PORT'),
        }
}

DATABASES['default']['ATOMIC_REQUESTS'] = True