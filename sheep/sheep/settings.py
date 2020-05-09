"""
Django settings for sheep project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

from django_redis import get_redis_connection


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'api'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nog-m-%lwpued&hxe6v^c9+m_b=dfe!7atv@^vmq&_*-980h=n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 是否为测试环境
DEVELOP = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'django_filters',
    'debug_toolbar',
    'mptt',
    'corsheaders',
    'commands.apps.CommandsConfig',
    'apps.user.apps.UserConfig',
    'apps.post.apps.PostConfig',
    'apps.operate.apps.OperateConfig',
    'apps.other.apps.OtherConfig'
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'utils.middleware.DRFCodeMiddleware'
]


ROOT_URLCONF = 'sheep.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'sheep.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sheep',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'oracle',
        # 使用mysql的innodb引擎,MyISAM虽快但没有事务rollback
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;',
                    'charset': 'utf8mb4', },
        "CONN_MAX_AGE": 600,
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8_general_ci',
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
# [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

DATETIME_FORMAT = 'Y-m-d H:i:s'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# 指定导出的静态文件存放目录
STATIC_ROOT = os.path.join(BASE_DIR, 'www')

# 用户上传得静态资源
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#设置可以跨域访问
CORS_ORIGIN_ALLOW_ALL = True

# 跨域所能请求的域名
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:*',
    'https://127.0.0.1:*',
    'http://*:*',
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'tk'
)

AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = (
    'apps.user.authentication.UserModelBackend',
)

PASSWORD_HASHERS = [
    'apps.user.hashers.SHA256',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
# 超管手机号
ADMIN_PHONE = []

# channels配置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        "ROUTING": "api.routing.channel_routing",
    },
}
ASGI_APPLICATION = 'sheep.asgi.application'

# rest framework 配置
REST_FRAMEWORK = \
    {
        'DEFAULT_PERMISSION_CLASSES': (
            'apps.user.permission.IsLoginUser',
                                      ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'apps.user.authentication.TokenAuthentication',
        ),
        # 'UNAUTHENTICATED_USER':lambda :'匿名用户'
        # 'DEFAULT_THROTTLE_CLASSES': (
        # 'rest_framework.throttling.AnonRateThrottle',
        # 'rest_framework.throttling.UserRateThrottle'
        #                           ),
        # 'DEFAULT_THROTTLE_RATES': {
        # 'anon': '1/minute',
        # 'user': '1/minute'        },
        'DATETIME_FORMAT': "%Y-%m-%d %H:%M",
        'HTML_SELECT_CUTOFF': 10000,
        'HTML_SELECT_CUTOFF_TEXT': '太多了,我加载不出来了',
        # 'EXCEPTION_HANDLER': 'utils.exceptions.main'
    }


CACHES = {
    'default': {
        'BACKEND': "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        'TIMEOUT': 600,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            #默认解码
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
        }
    },
    'user': {
        'BACKEND': "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/10",
        'TIMEOUT': 600,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
        }
    },
}

# Token配置
TOKEN = {
    'FRAME': 'django',
    'TOKEN_SECURITY_KEY': b'pBy0j5_m6qqTOXElHSs0OlfV5qiYhqHkEvwLtdrXZ5o=',
    'TOKEN_EXPIRES': 7*24*3600,
    'TOKEN_REDIS': get_redis_connection('user'),
    'TOKEN_NAME': 'tk'
}


# django-debug-toolbar配置
# 调试工具的ip
INTERNAL_IPS = ['127.0.0.1', ]
DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}

try:
    from .local_setting import *

    from . import local_setting

    if hasattr(local_setting, 'CUSTOM_INSTALLED_APPS'):
        INSTALLED_APPS += local_setting.CUSTOM_INSTALLED_APPS
    if hasattr(local_setting, 'CUSTOM_MIDDLEWARE_CLASSES'):
        MIDDLEWARE += local_setting.CUSTOM_MIDDLEWARE
except ImportError:
    pass
