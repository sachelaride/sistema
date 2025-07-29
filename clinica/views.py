# Importa funções e classes do Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Clinica, Paciente, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo
from .forms import UserForm, ClinicaForm, PacienteForm, AgendamentoForm, AtendimentoForm, PastaDocumentoForm, DocumentoArquivoForm
from .permissions import check_perfil
from django.contrib import messages
from django.db import models
# Importa módulo de logging
import logging

# Configura o logger para auditoria
logger = logging.getLogger('clinica')

# View para a página inicial
def index(request):
    return render(request, 'index.html')

# View para login
def login_view(request):
    if request.method == 'POST':                        # Verifica se é um POST
        username = request.POST.get('username')         # Obtém o username (RGM/CPF)
        password = request.POST.get('password')         # Obtém a senha
        user = authenticate(request, username=username, password=password) # Autentica
        if user is not None:
            login(request, user)                       # Faz login
            logger.info(f"Usuário {user.username} fez login.") # Registra no log
            return redirect('clinica:index')                   # Redireciona para a página inicial
        messages.error(request, "Credenciais inválidas.") # Mensagem de erro
    return render(request, 'login.html')               # Renderiza o template de login

# View para logout
def logout_view(request):
    logout(request)                                    # Faz logout
    return redirect('clinica:login')                           # Redireciona para login

# View para listar usuários (restrita a coordenadores)
@login_required
@check_perfil(['COORDENADOR'])
def user_list(request):
    users = User.objects.all()                         # Obtém todos os usuários
    return render(request, 'user_list.html', {'users': users}) # Renderiza a lista

# View para criar usuários
@login_required
@check_perfil(['COORDENADOR'])
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)                  # Cria formulário com dados do POST
        if form.is_valid():
            user = form.save(commit=False)             # Salva sem commit
            user.set_password(form.cleaned_data['password']) # Define a senha
            user.save()                                # Salva o usuário
            logger.info(f"Usuário {user.username} criado por {request.user.username}.") # Log
            return redirect('clinica:user_list')               # Redireciona para a lista
    else:
        form = UserForm()                              # Cria formulário vazio
    return render(request, 'user_form.html', {'form': form}) # Renderiza o formulário

# View para listar clínicas
@login_required
def clinica_list(request):
    clinicas = Clinica.objects.all()                   # Obtém todas as clínicas
    return render(request, 'clinica_list.html', {'clinicas': clinicas}) # Renderiza

# View para criar clínicas
@login_required
@check_perfil(['COORDENADOR'])
def clinica_create(request):
    if request.method == 'POST':
        form = ClinicaForm(request.POST)               # Cria formulário com dados do POST
        if form.is_valid():
            form.save()                                # Salva a clínica
            logger.info(f"Clínica criada por {request.user.username}.") # Log
            return redirect('clinica:clinica_list')            # Redireciona
    else:
        form = ClinicaForm()                           # Cria formulário vazio
    return render(request, 'clinica_form.html', {'form': form}) # Renderiza

# View para listar pacientes com busca
@login_required
def paciente_list(request):
    pacientes = Paciente.objects.all()                 # Obtém todos os pacientes
    if request.GET.get('search'):                      # Verifica se há busca
        search = request.GET.get('search')
        # Filtra por nome, CPF ou telefone
        pacientes = pacientes.filter(models.Q(nome__icontains=search) | models.Q(cpf__icontains=search) | models.Q(telefone__icontains=search))
    return render(request, 'paciente_list.html', {'pacientes': pacientes}) # Renderiza

# View para criar pacientes
@login_required
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)              # Cria formulário com dados do POST
        if form.is_valid():
            form.save()                                # Salva o paciente
            logger.info(f"Paciente criado por {request.user.username}.") # Log
            return redirect('clinica:paciente_list')           # Redireciona
    else:
        form = PacienteForm()                          # Cria formulário vazio
    return render(request, 'paciente_form.html', {'form': form}) # Renderiza

# View para listar agendamentos
@login_required
def agendamento_list(request):
    agendamentos = Agendamento.objects.all()           # Obtém todos os agendamentos
    return render(request, 'agendamento_list.html', {'agendamentos': agendamentos}) # Renderiza

# View para criar agendamentos
@login_required
@check_perfil(['ATENDENTE', 'PROFESSOR', 'COORDENADOR'])
def agendamento_create(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)           # Cria formulário com dados do POST
        if form.is_valid():
            form.save()                                # Salva o agendamento
            logger.info(f"Agendamento criado por {request.user.username}.") # Log
            return redirect('clinica:agendamento_list')        # Redireciona
    else:
        form = AgendamentoForm()                       # Cria formulário vazio
    return render(request, 'agendamento_form.html', {'form': form}) # Renderiza

# View para listar atendimentos
@login_required
def atendimento_list(request):
    atendimentos = Atendimento.objects.all()           # Obtém todos os atendimentos
    return render(request, 'atendimento_list.html', {'atendimentos': atendimentos}) # Renderiza

# View para criar atendimentos
@login_required
@check_perfil(['PROFESSOR', 'ALUNO'])
def atendimento_create(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)           # Cria formulário com dados do POST
        if form.is_valid():
            atendimento = form.save(commit=False)      # Salva sem commit
            # Verifica se aluno tem professor monitor
            if request.user.perfil == 'ALUNO' and not atendimento.professor_monitor:
                messages.error(request, "Professor monitor é obrigatório para alunos.")
                return render(request, 'atendimento_form.html', {'form': form})
            atendimento.save()                          # Salva o atendimento
            logger.info(f"Atendimento criado por {request.user.username}.") # Log
            return redirect('clinica:atendimento_list')        # Redireciona
    else:
        form = AtendimentoForm()                       # Cria formulário vazio
    return render(request, 'atendimento_form.html', {'form': form}) # Renderiza

# View para listar documentos
@login_required
def documento_list(request):
    documentos = DocumentoArquivo.objects.all()         # Obtém todos os documentos
    return render(request, 'documento_list.html', {'documentos': documentos}) # Renderiza

# View para criar documentos
@login_required
def documento_create(request):
    if request.method == 'POST':
        form = DocumentoArquivoForm(request.POST, request.FILES) # Cria formulário com arquivos
        if form.is_valid():
            documento = form.save(commit=False)         # Salva sem commit
            # Verifica duplicatas por hash
            if DocumentoArquivo.objects.filter(hash_arquivo=documento.hash_arquivo).exists():
                messages.error(request, "Arquivo já existe.")
                return render(request, 'documento_form.html', {'form': form})
            documento.save()                           # Salva o documento
            logger.info(f"Documento enviado por {request.user.username}.") # Log
            return redirect('clinica:documento_list')          # Redireciona
    else:
        form = DocumentoArquivoForm()                  # Cria formulário vazio
    return render(request, 'documento_form.html', {'form': form}) # Renderiza
