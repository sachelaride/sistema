# Arquivo: sistema_clinicas/asgi.py
# Configuração ASGI para o projeto

import os
from django.core.asgi import get_asgi_application

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_clinicas.settings')

# Obtém a aplicação ASGI
application = get_asgi_application()
