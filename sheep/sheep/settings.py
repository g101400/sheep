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
import time
from multiprocessing import cpu_count

from celery.schedules import crontab
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

ALLOWED_HOSTS = ['*']

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
    'django_extensions',
    'mptt',
    'corsheaders',
    'django_celery_results',
    # celery自动导入不支持 apps.user.apps.UserConfig这种方式
    'commands',
    'apps.user.apps.UserConfig',
    'apps.post',
    'apps.operate',
    'apps.other',
    'apps.index',
    'apps.search'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.drf_code.DRFCodeMiddleware',
    'middleware.record_logging.RecordLoggingMiddleware'
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
# MEDIA_DIRS = ['portrait', 'post_image', 'post_mavon', 'post_tinymce']

# 设置可以跨域访问
CORS_ORIGIN_ALLOW_ALL = True
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True
# 跨域所能请求的域名
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:3000',
    'http://*:*',
    'http://localhost:3000',
    'https://*:*'
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
    'tk',
    'u-host'
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
        "ROUTING": "sheep.routing.application",
    },
}
ASGI_APPLICATION = 'sheep.routing.application'
WSGI_APPLICATION = 'sheep.wsgi.application'

# rest framework 配置
REST_FRAMEWORK = \
    {
        'DEFAULT_PERMISSION_CLASSES': (
            'apps.user.permission.IsLoginUser',
                                      ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'apps.user.authentication.TokenAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
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
        'HTML_SELECT_CUTOFF': 200,
        'HTML_SELECT_CUTOFF_TEXT': '太多了,我加载不出来了',
        # 'EXCEPTION_HANDLER': 'utils.exceptions.main'
    }

# REST_FRAMEWORK_EXTENSIONS 设置
REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_USE_CACHE": "restframework_extensions",
    "DEFAULT_CACHE_RESPONSE_TIMEOUT": 30*60
}

REDIS_HOST = 'redis://127.0.0.1:6379/'
CACHES = {
    'default': {
        'BACKEND': "django_redis.cache.RedisCache",
        "LOCATION": REDIS_HOST + "1",
        'TIMEOUT': 2000,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
        }
    },
    'restframework_extensions': {
        # 不用decode_response
        'BACKEND': "django_redis.cache.RedisCache",
        "LOCATION": REDIS_HOST + "2",
        'TIMEOUT': 2000,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        }
    },
    'user': {
        'BACKEND': "django_redis.cache.RedisCache",
        "LOCATION": REDIS_HOST + "10",
        'TIMEOUT': 2000,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
        }
    },
}
from django_redis import get_redis_connection
USER_REDIS = get_redis_connection('user')

# celery配置
CELERY_BROKER_BACKEND = "redis"
# 设置broker任务队列所在位置
CELERY_BROKER_URL = REDIS_HOST + "3"
# 并发worker数
CELERY_WORKER_CONCURRENCY = cpu_count()
# celery的时区设置
CELERY_TIMEZONE = TIME_ZONE
# 防止celery的死锁情况出现
# CELERYD_FORCE_EXECV = True
# 每个worker最多执行内核数*10个任务就会被销毁，可防止内存泄露
CELERY_WORKER_MAX_TASKS_PER_CHILD = cpu_count() * 10
# 硬超时,会被强杀
CELERY_TASK_TIME_LIMIT = 3*60
# 软超时,会抛异常
CELERY_TASK_SOFT_TIME_LIMIT = 2*60+30
CELERY_REDIS_CONNECT_RETRY = True
CELERY_TASK_SEND_SENT_EVENT = True
# CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 31104000}
# 默认worker使用的队列
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'

# celery-result 配置
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = REDIS_HOST + "4"
CELERY_RESULT_EXPIRES = 60*24*2
CELERY_RESULT_CACHE_MAX = 3
CELERY_BEAT_SCHEDULE = {
    'clear-celery-results': {
        # 由于选用数据库作为result的存储后端,result不会自动清除,所以手写一个定时任务清除
        'task': 'apps.other.tasks.clear_celery_results',
        'schedule': crontab(minute=f"*/{CELERY_RESULT_EXPIRES}"),
    },
}

# Token配置
TOKEN = {
    'FRAME': 'django',
    'TOKEN_SECURITY_KEY': b'pBy0j5_m6qqTOXElHSs0OlfV5qiYhqHkEvwLtdrXZ5o=',
    'TOKEN_EXPIRES': 7*24*3600,
    'TOKEN_REDIS': USER_REDIS,
    'TOKEN_NAME': 'token'
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

# 日志配置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False if DEBUG else True,
    'formatters': {
        'verbose': {
            'format':  # '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                '%(asctime)s %(levelname)s %(thread)d %(process)d %(funcName)s %(lineno)d - %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'simple',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'verbose',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',  # 设置默认编码
        },
        'script': {
            'level': 'DEBUG',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "script-{}.log".format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'default', 'info', 'error'],
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'script': {
            'handlers': ['script'],
            'level': 'INFO',
            'propagate': False
        },
    }
}


if DEBUG:
    EXTRA_MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    EXTRA_INSTALL_APPS = [
        'debug_toolbar',
    ]
    MIDDLEWARE.extend(EXTRA_MIDDLEWARE)
    INSTALLED_APPS.extend(EXTRA_INSTALL_APPS)

# 百度api
BD_API_LOCATION_IP_URL = "http://api.map.baidu.com/location/ip"
BD_API_MAP_PARAMS = {
    'ak': '个人自己的ak',
}

# 七牛云配置
QI_NIU_CLOUD = {
    'auth': {
        'access_key': '用户ak',
        'secret_key': '用户sk'
    },
    'base_url': {
        '桶名': '桶域名'
    },
    'expires': 3600
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
