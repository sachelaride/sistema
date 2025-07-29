import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# Chave de segurança (gerada aleatoriamente para este exemplo; substitua por uma chave única)
SECRET_KEY = 'django-insecure-@k#9z2h5j7p!qwe4rty8uio0pasdfghjklzxcvbnm1234567890'


# Debug and Allowed Hosts
DEBUG = True  # Set to True for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.0.136', 'testserver']
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.0.136']  # Add server IP if needed

# Modelo de Usuário Personalizado
AUTH_USER_MODEL = 'clinica.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Aplicativos Instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clinica.apps.ClinicaConfig',
#    'clinica',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração de URLs
ROOT_URLCONF = 'sistema_clinicas.urls'

# Configuração de Templates
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
            ],
        },
    },
]

# Arquivos Estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIR = [ 
        BASE_DIR / 'static',
]

# Banco de Dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'audit.log',
        },
    },
    'loggers': {
        'clinica': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
