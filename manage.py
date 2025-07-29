#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# Define o interpretador Python a ser usado

import os
import sys
# Importa os módulos necessários para configurar o ambiente

def main():
    """Run administrative tasks."""
    # Define a função principal que executa as tarefas administrativas
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_clinicas.settings')
    # Configura a variável de ambiente para apontar para o módulo de configurações do projeto
    try:
        from django.core.management import execute_from_command_line
        # Importa a função que executa comandos do Django
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        # Lança um erro se o Django não estiver instalado ou acessível
    execute_from_command_line(sys.argv)
    # Executa o comando passado via linha de comando (ex.: runserver, migrate)

if __name__ == '__main__':
    main()
    # Executa a função main() se o script for chamado diretamente
