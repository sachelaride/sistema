# Importa módulos do Django para modelos
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Importa hashlib para cálculo de hash SHA-256
import hashlib
import os
from datetime import datetime

#Modelo de Prontuario
#from django.db import models
#from django.conf import settings
#import hashlib
#import os
#from datetime import datetime

#class Prontuario(models.Model):
#    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='prontuarios')
#    atendimento = models.ForeignKey('Atendimento', on_delete=models.CASCADE, related_name='prontuarios')
#    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'perfil': 'PROFESSOR'})
#    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'perfil': 'COORDENADOR'}, related_name='prontuarios_coordenador')
#    data_criacao = models.DateTimeField(auto_now_add=True)
#    observacoes = models.TextField(blank=True)
#    arquivo = models.FileField(upload_to='uploads/prontuarios/%Y/%m/%d/', null=True, blank=True)
#    hash_arquivo = models.CharField(max_length=64, blank=True)
#
#    def save(self, *args, **kwargs):
#        if self.arquivo:
#            # Calcular hash SHA-256 para evitar duplicatas
#            sha256_hash = hashlib.sha256()
#            for chunk in self.arquivo.chunks():
#                sha256_hash.update(chunk)
#            self.hash_arquivo = sha256_hash.hexdigest()
#        super().save(*args, **kwargs)
#
#    class Meta:
#        permissions = [
#            ('view_prontuario', 'Can view prontuario'),
#            ('add_prontuario', 'Can add prontuario'),
#            ('change_prontuario', 'Can change prontuario'),
#        ]
#
#    def __str__(self):
#        return f"Prontuário de {self.paciente} - {self.data_criacao}"


class Prontuario(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='prontuarios')
    atendimento = models.ForeignKey('Atendimento', on_delete=models.CASCADE, related_name='prontuarios')
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'perfil': 'PROFESSOR'})
    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'perfil': 'COORDENADOR'}, related_name='prontuarios_coordenador')
    data_criacao = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='uploads/prontuarios/%Y/%m/%d/', null=True, blank=True)
    hash_arquivo = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if self.arquivo:
            sha256_hash = hashlib.sha256()
            for chunk in self.arquivo.chunks():
                sha256_hash.update(chunk)
            self.hash_arquivo = sha256_hash.hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        # Removidas permissões redundantes
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'

    def __str__(self):
        return f"Prontuário de {self.paciente} - {self.data_criacao}"





# Modelo de usuário personalizado
class User(AbstractUser):
    # Escolhas para o campo de perfil
    PERFIL_CHOICES = (
        ('ATENDENTE', 'Atendente'),
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('COORDENADOR', 'Coordenador'),
    )
    # Campo para RGM (identificador único)
    rgm = models.CharField(max_length=20, unique=True, blank=True, null=True)
    # Campo para perfil do usuário
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, blank=True)
    # Relacionamento com clínica (pode ser nulo)
    clinica = models.ForeignKey('Clinica', on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='clinica_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='clinica_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )
    # Representação em string do usuário
    def __str__(self):
        return f"{self.username} ({self.perfil})"

# Modelo para clínicas
class Clinica(models.Model):
    nome = models.CharField(max_length=100)       # Nome da clínica
    endereco = models.TextField()                 # Endereço da clínica
    telefone = models.CharField(max_length=15, blank=True) # Telefone (opcional)

    # Representação em string
    def __str__(self):
        return self.nome

# Modelo para pacientes
class Paciente(models.Model):
    nome = models.CharField(max_length=100)       # Nome do paciente
    # CPF com validação de formato
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF deve estar no formato XXX.XXX.XXX-XX')]
    )
    data_nascimento = models.DateField()          # Data de nascimento
    email = models.EmailField(unique=True, blank=True, null=True) # Email (opcional)
    telefone = models.CharField(max_length=15, blank=True) # Telefone (opcional)
    endereco = models.TextField(blank=True)       # Endereço (opcional)
    responsavel_legal = models.CharField(max_length=100, blank=True) # Responsável legal (para menores)

    # Representação em string
    def __str__(self):
        return self.nome

# Modelo para agendamentos
class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # Paciente associado
    medico = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'perfil': 'PROFESSOR'}) # Médico (apenas professores)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_aluno', limit_choices_to={'perfil': 'ALUNO'}, null=True) # Aluno (opcional)
    data = models.DateTimeField()                 # Data e hora do agendamento
    # Status do agendamento
    status = models.CharField(
        max_length=20,
        choices=[('AGENDADO', 'Agendado'), ('CONCLUIDO', 'Concluído'), ('CANCELADO', 'Cancelado')],
        default='AGENDADO'
    )

    # Representação em string
    def __str__(self):
        return f"Agendamento de {self.paciente.nome} com {self.medico.username} em {self.data}"

# Modelo para atendimentos
class Atendimento(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE) # Agendamento associado
    professor_monitor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'perfil': 'PROFESSOR'}) # Professor monitor
    observacoes = models.TextField(blank=True)     # Observações do atendimento
    data_inicio = models.DateTimeField(auto_now_add=True) # Data de início
    data_fim = models.DateTimeField(null=True, blank=True) # Data de fim (opcional)
    # Status do atendimento
    status = models.CharField(
        max_length=20,
        choices=[('INICIADO', 'Iniciado'), ('FINALIZADO', 'Finalizado')],
        default='INICIADO'
    )

    # Representação em string
    def __str__(self):
        return f"Atendimento de {self.agendamento.paciente.nome} por {self.professor_monitor.username}"

# Modelo para pastas de documentos
class PastaDocumento(models.Model):
    nome = models.CharField(max_length=100)       # Nome da pasta
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE) # Clínica associada
    created_at = models.DateTimeField(auto_now_add=True) # Data de criação

    # Representação em string
    def __str__(self):
        return self.nome

# Modelo para arquivos de documentos
class DocumentoArquivo(models.Model):
    pasta = models.ForeignKey(PastaDocumento, on_delete=models.CASCADE) # Pasta associada
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True) # Paciente associado (opcional)
    arquivo = models.FileField(upload_to='uploads/%Y/%m/%d/') # Arquivo com caminho dinâmico
    hash_arquivo = models.CharField(max_length=64) # Hash SHA-256 do arquivo
    uploaded_at = models.DateTimeField(auto_now_add=True) # Data de upload

    # Sobrescreve o método save para calcular o hash
    def save(self, *args, **kwargs):
        if self.arquivo:
            self.hash_arquivo = self.calculate_hash() # Calcula o hash antes de salvar
        super().save(*args, **kwargs)

    # Calcula o hash SHA-256 do arquivo
    def calculate_hash(self):
        sha256 = hashlib.sha256()                # Inicializa o objeto SHA-256
        for chunk in self.arquivo.chunks():     # Lê o arquivo em pedaços
            sha256.update(chunk)
        return sha256.hexdigest()               # Retorna o hash em hexadecimal

    # Representação em string
    def __str__(self):
        return f"Arquivo em {self.pasta.nome}"
