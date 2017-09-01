from sican.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']


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