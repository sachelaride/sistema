# Importa o módulo de administração do Django
from django.contrib import admin
# Importa os modelos do aplicativo clinica
from .models import User, Clinica, Paciente, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo

# Registra os modelos no painel administrativo
admin.site.register(User)
admin.site.register(Clinica)
admin.site.register(Paciente)
admin.site.register(Agendamento)
admin.site.register(Atendimento)
admin.site.register(PastaDocumento)
admin.site.register(DocumentoArquivo)
