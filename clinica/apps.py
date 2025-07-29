# Arquivo: clinica/apps.py
# Configuração do aplicativo Django 'clinica'

from django.apps import AppConfig  # Importa a classe base para configuração de aplicativos Django

class ClinicaConfig(AppConfig):
    # Define o tipo de chave primária padrão para os modelos do aplicativo
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Define o nome do aplicativo, que deve corresponder ao nome do diretório
    name = 'clinica'
