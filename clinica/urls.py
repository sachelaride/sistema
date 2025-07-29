from django.urls import path
from . import views

app_name = 'clinica'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/new/', views.user_create, name='user_create'),
    path('clinicas/', views.clinica_list, name='clinica_list'),
    path('clinicas/new/', views.clinica_create, name='clinica_create'),
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/new/', views.paciente_create, name='paciente_create'),
    path('agendamentos/', views.agendamento_list, name='agendamento_list'),
    path('agendamentos/new/', views.agendamento_create, name='agendamento_create'),
    path('atendimentos/', views.atendimento_list, name='atendimento_list'),
    path('atendimentos/new/', views.atendimento_create, name='atendimento_create'),
    path('documentos/', views.documento_list, name='documento_list'),
    path('documentos/new/', views.documento_create, name='documento_create'),
    path('prontuarios/', views.prontuario_list, name='prontuario_list'),
    path('prontuarios/new/', views.prontuario_create, name='prontuario_create'),
]
