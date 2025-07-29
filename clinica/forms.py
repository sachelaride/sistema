# Importa o módulo de formulários do Django
from django import forms
# Importa os modelos do aplicativo clinica
from .models import User, Clinica, Paciente, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo, Prontuario


#Formulario para Pronturario
class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ['paciente', 'atendimento', 'professor', 'coordenador', 'observacoes', 'arquivo']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 5}),
        }

# Formulário para criação de usuários
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'rgm', 'perfil', 'clinica', 'password'] # Campos do formulário
        widgets = {'password': forms.PasswordInput()} # Widget para senha

# Formulário para clínicas
class ClinicaForm(forms.ModelForm):
    class Meta:
        model = Clinica
        fields = ['nome', 'endereco', 'telefone'] # Campos do formulário

# Formulário para pacientes
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'email', 'telefone', 'endereco', 'responsavel_legal']
        widgets = {'data_nascimento': forms.DateInput(attrs={'type': 'date'})} # Widget para data

# Formulário para agendamentos
class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'medico', 'aluno', 'data', 'status']
        widgets = {'data': forms.DateTimeInput(attrs={'type': 'datetime-local'})} # Widget para data/hora

# Formulário para atendimentos
class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['agendamento', 'professor_monitor', 'observacoes', 'status']

# Formulário para pastas de documentos
class PastaDocumentoForm(forms.ModelForm):
    class Meta:
        model = PastaDocumento
        fields = ['nome', 'clinica']

# Formulário para arquivos de documentos
class DocumentoArquivoForm(forms.ModelForm):
    class Meta:
        model = DocumentoArquivo
        fields = ['pasta', 'paciente', 'arquivo']
