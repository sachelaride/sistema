# Arquivo: sistema_clinicas/wsgi.py
# Configuração WSGI para o projeto

import os
from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_clinicas.settings')

# Obtém a aplicação WSGI
application = get_wsgi_application()
