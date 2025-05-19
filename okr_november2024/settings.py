import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tq(95gx-&2y-!==pxlw+y*)g-##$4493hj-vzuuc&lg2*0dce='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
    'cart.apps.CartConfig',
    'rest_framework',
    'drf_spectacular',
    'oauth2_provider',

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


ROOT_URLCONF = 'okr_november2024.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'okr_november2024.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'default_db'),
        'USER': os.environ.get('POSTGRES_USER', 'default_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'default_password'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

OAUTH2_PROVIDER = {
    #'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,
    'ALLOW_PKCE_GRANT_TYPE': True,
    'DEFAULT_SCOPES': ['read', 'write'],
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http', 'https'],
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups',
    },
    # 'GRANT_TYPES': [
    #     'authorization_code',
    #     'password',
    #     'client_credentials',
    #     'refresh_token',
    # ],
}

OAUTH2_CLIENT_ID = os.environ.get('OAUTH2_CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.environ.get('OAUTH2_CLIENT_SECRET')

SPECTACULAR_SETTINGS = {
    'TITLE': 'okr_november2024',
    'DESCRIPTION': 'API documentation by Elvira Karpova.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'AUTHENTICATION_WHITELIST': [],
    'SWAGGER_UI_OAUTH2_CONFIG': {
        'clientId': os.environ.get('OAUTH2_CLIENT_ID'),
        'clientSecret': os.environ.get('OAUTH2_CLIENT_SECRET'),
        'appName': 'okr_november2024',
        'scopes': ['read', 'write'],
        'usePkceWithAuthorizationCodeGrant': True,
    },
    'SECURITY': [
        {'BearerAuth': []},
        {'OAuth2': []},
    ],
    'SECURITY_SCHEMES': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
        },
        'OAuth2': {
            'type': 'oauth2',
            'flows': {
                'password': {
                    'tokenUrl': 'http://127.0.0.1:8007/o/token/',
                    'scopes': {
                        'read': 'Read access',
                        'write': 'Write access',
                    },
                },
                'authorizationCode': {
                    'authorizationUrl': 'http://127.0.0.1:8007/o/authorize/',
                    'tokenUrl': 'http://127.0.0.1:8007/o/token/',
                    'scopes': {
                        'read': 'Read access',
                        'write': 'Write access',
                    },
                },
            },
        },
    },
}
