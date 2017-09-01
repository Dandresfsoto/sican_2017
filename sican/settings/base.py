"""
Sican 2.0
"""

import os
from celery.schedules import crontab
import locale
import sys
if sys.platform in ['win32']:
    locale.setlocale(locale.LC_ALL, "eso")

if sys.platform in ['linux2']:
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'


CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'Carga Productos': {
        'task': 'informes.tasks.compilado_matriz_chequeo',
        'schedule': crontab(minute=0,hour=0),
        'args': (),
    },
    #'verificando-archivos-transportes': {
    #    'task': 'financiera.tasks.verificar_archivos',
    #    'schedule': crontab(),
    #    'args': (),
    #},
    'Nueva-semana-cronograma': {
        'task': 'informes.tasks.nueva_semana',
        'schedule': crontab(minute=0,hour=0, day_of_week=1),
        'args': (),
    },
    'Recordatorio-Cronograma': {
        'task': 'requerimientos.tasks.recordatorio_requerimiento',
        'schedule': crontab(minute=0, hour=8),
        'args': (),
    },
}



EMAIL_HOST = os.getenv('SICAN_EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('SICAN_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('SICAN_EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('SICAN_EMAIL_PORT')
DEFAULT_FROM_EMAIL = os.getenv('SICAN_DEFAULT_FROM_EMAIL')
RECURSO_HUMANO_EMAIL = 'recursohumano@asoandes.org'
EMAIL_USE_TLS = True
API_KEY_SMS = os.getenv('SICAN_API_KEY_SMS')

LOGIN_URL = '/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8ijem+go0u+@npn$0vjym_l3jfs*o$#ic0&e-6@d3c5p8^s#sp'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = [('Diego Fonseca','sistemas@asoandes.org')]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]


LOCAL_APPS = [
    'usuarios',
    'inbox',
    'rest',
    'administrativos',
    'region',
    'rh',
    'cargos',
    'bancos',
    'adminuser',
    'permisos_sican',
    'formadores',
    'departamentos',
    'municipios',
    'secretarias',
    'radicados',
    'bases',
    'docentes',
    'preinscripcion',
    'financiera',
    'informes',
    'formacion',
    'encuestas',
    'productos',
    'messenger',
    'lideres',
    'acceso',
    'contratos',
    'matrices',
    'evidencias',
    'negociadores',
    'requerimientos',
    'sicantelegram',
    'beneficiarios',
    'vigencia2017',
]

THIRD_PARTY_APPS = [
    'mail_templated',
    'django_cleanup',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    "permabots",
    #'channels',
    'guardian',
    'crispy_forms',
    'smart_selects',
    'django_tables2',
    'sslserver',
]


CRISPY_TEMPLATE_PACK = 'bootstrap3'

#CHANNEL_LAYERS = {
#    "default": {
#        "BACKEND": "asgi_redis.RedisChannelLayer",
#        "CONFIG": {
#            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
#        },
#        "ROUTING": "inbox.routing.channel_routing",
#    },
#}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGE_SIZE': 10,
    'UNICODE_JSON': False
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sican.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'sican.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True







STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')


AUTH_USER_MODEL = "usuarios.User"

TELEGRAM_BOT_HANDLERS_CONF = "sicantelegram.bot_handlers"
TELEGRAM_BOT_TOKEN_EXPIRATION = "2"

SITE_ID=1