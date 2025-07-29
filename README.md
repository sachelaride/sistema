<<<<<<< HEAD
# Sistema de Clínicas

Sistema de gerenciamento de clínicas desenvolvido em Django, com suporte a autenticação, gestão de usuários, clínicas, pacientes, agendamentos, atendimentos e documentos. O sistema é responsivo, utiliza Bootstrap 5.3 para a interface e PostgreSQL como banco de dados principal, com suporte a SQLite para testes.

## Requisitos

- **Sistema Operacional**: Debian Linux (testado no Debian 11/12)
- **Python**: 3.8 ou superior
- **PostgreSQL**: 13 ou superior
- **Ferramentas**: `pip`, `rar`, `unrar`
- **Dependências Python**:
  - Django 4.2.7
  - psycopg2-binary 2.9.9

## Instalação no Debian Linux

Siga os passos abaixo para configurar e executar o sistema em um ambiente Debian Linux.

1. **Atualize o sistema**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instale as dependências do sistema**:
   - Instale Python, pip, ambiente virtual, PostgreSQL e utilitários RAR:
     ```bash
     sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib rar unrar -y
     ```

3. **Configure o PostgreSQL**:
   - Inicie e habilite o serviço PostgreSQL:
     ```bash
     sudo systemctl start postgresql
     sudo systemctl enable postgresql
     ```
   - Crie o banco de dados e configure o usuário:
     ```bash
     sudo -u postgres psql -c "CREATE DATABASE sistema_clinicas;"
     sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
     sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sistema_clinicas TO postgres;"
     ```

4. **Descompacte o projeto**:
   - Descompacte o arquivo RAR fornecido (`sistema_clinicas_django.rar`):
     ```bash
     unrar x sistema_clinicas_django.rar
     cd sistema_clinicas
     ```

5. **Crie e ative um ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Instale as dependências do projeto**:
   - As dependências estão listadas em `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

7. **Crie diretórios para uploads e logs**:
   - Crie as pastas necessárias e ajuste permissões:
     ```bash
     mkdir -p uploads/01 uploads/02 logs
     chmod -R 775 uploads logs
     ```

8. **Aplique as migrações do banco de dados**:
   - Crie e aplique as migrações para configurar o banco:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

9. **Popule o banco com dados de teste**:
   - Execute o script para adicionar dados de exemplo:
     ```bash
     python clinica/populate_db.py
     ```

10. **Crie um superusuário**:
    - Crie um usuário administrador para acessar o painel admin:
      ```bash
      python manage.py createsuperuser
      ```

11. **Coletar arquivos estáticos**:
    - Colete os arquivos estáticos (CSS, etc.) para o servidor:
      ```bash
      python manage.py collectstatic
      ```

12. **Inicie o servidor**:
    - Inicie o servidor de desenvolvimento:
      ```bash
      python manage.py runserver 0.0.0.0:8000
      ```
    - Acesse o sistema em: `http://localhost:8000/`
    - Acesse o painel admin em: `http://localhost:8000/admin/`

## Funcionalidades

O sistema implementa as seguintes funcionalidades, conforme as especificações:

- **Autenticação**: Login com RGM ou CPF e senha, com permissões granulares baseadas em perfis (Atendente, Aluno, Professor, Coordenador).
- **Gestão de Usuários**: CRUD de usuários, restrito a coordenadores, com validação de RGM e associação a clínicas.
- **Gestão de Clínicas**: Cadastro e listagem de clínicas, com controle de acesso por perfil.
- **Gestão de Pacientes**: Cadastro unificado de pacientes, busca global por nome, CPF ou telefone, e suporte a responsáveis legais para menores.
- **Agendamentos**: Sistema de agendamento com médicos (professores) e alunos (opcional), com status (Agendado, Concluído, Cancelado).
- **Atendimentos**: Gestão de atendimentos vinculados a agendamentos, com obrigatoriedade de professor monitor para alunos.
- **Documentos**: Upload de arquivos com organização em pastas, verificação de duplicatas por hash SHA-256, e suporte a download/visualização.
- **Interface**: Interface web responsiva usando Bootstrap 5.3, com navegação, formulários e tabelas.
- **Logs de Auditoria**: Registro de ações (login, criação de registros, upload de documentos) em `logs/audit.log`.

## Dados de Teste

O script `clinica/populate_db.py` adiciona os seguintes dados de exemplo:

- **Usuários**:
  - `admin` (Coordenador, RGM: RGM0001, senha: `lizard1240king`)
  - `professor1` (Professor, RGM: RGM0002, senha: `senha123`)
  - `aluno1` (Aluno, RGM: RGM0003, senha: `senha123`)
  - `atendente1` (Atendente, RGM: RGM0004, senha: `senha123`)
- **Clínicas**:
  - Clínica Central (Rua Principal, 100, São Paulo, SP)
  - Clínica Norte (Avenida Norte, 200, São Paulo, SP)
- **Pacientes**:
  - Ana Silva (CPF: 123.456.789-00, adulto)
  - João Santos (CPF: 987.654.321-00, menor com responsável legal: Maria Santos)
- **Agendamentos**:
  - 2 agendamentos para os próximos dias (um com aluno, outro sem)
- **Atendimentos**:
  - 1 atendimento iniciado, vinculado ao primeiro agendamento
- **Pastas de Documentos**:
  - Documentos Gerais (Clínica Central)
  - Exames (Clínica Norte)

## Estrutura do Banco de Dados

- **User**: Modelo de usuário personalizado com RGM, perfil (Atendente, Aluno, Professor, Coordenador) e clínica associada.
- **Clinica**: Dados das clínicas (nome, endereço, telefone).
- **Paciente**: Dados dos pacientes com CPF único, data de nascimento, email, telefone, endereço e responsável legal.
- **Agendamento**: Agendamentos com paciente, médico (professor), aluno (opcional), data e status.
- **Atendimento**: Atendimentos vinculados a agendamentos, com professor monitor, observações, data de início/fim e status.
- **PastaDocumento**: Pastas para organização de documentos, associadas a clínicas.
- **DocumentoArquivo**: Arquivos com hash SHA-256, associados a pastas e pacientes, armazenados em `uploads/YYYY/MM/DD/`.

## Notas

- **Logs de Auditoria**: Todas as ações principais (login, criação de registros, upload de documentos) são registradas em `logs/audit.log`.
- **Arquivos de Upload**: Arquivos são salvos em `uploads/YYYY/MM/DD/`. As pastas `uploads/01` e `uploads/02` são criadas para compatibilidade com a estrutura inicial.
- **SQLite como Alternativa**: Para testes sem PostgreSQL, altere `DATABASES` em `sistema_clinicas/settings.py`:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```
  Após alterar, reaplique as migrações.

## Solução de Problemas

- **Erro de conexão com PostgreSQL**:
  - Verifique se o serviço está ativo:
    ```bash
    sudo systemctl status postgresql
    ```
  - Confirme as credenciais em `sistema_clinicas/settings.py` (usuário: `postgres`, senha: `postgres`, host: `localhost`, porta: `5432`).
  - Reinicie o serviço se necessário:
    ```bash
    sudo systemctl restart postgresql
    ```

- **Erro ao descompactar RAR**:
  - Certifique-se de que o `unrar` está instalado:
    ```bash
    sudo apt install unrar
    ```
  - Tente descompactar novamente:
    ```bash
    unrar x sistema_clinicas_django.rar
    ```

- **Permissões de arquivo**:
  - Se houver erros de permissão ao acessar `uploads` ou `logs`, ajuste as permissões:
    ```bash
    chmod -R 775 uploads logs
    ```

- **Erro ao instalar dependências**:
  - Verifique se o ambiente virtual está ativo (`source venv/bin/activate`).
  - Atualize o pip:
    ```bash
    pip install --upgrade pip
    ```
  - Reinstale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

- **Erro ao aplicar migrações**:
  - Certifique-se de que o banco de dados está criado e acessível.
  - Remova migrações antigas (se necessário) e recrie:
    ```bash
    rm clinica/migrations/*.py
    python manage.py makemigrations
    python manage.py migrate
    ```

## Compactação do Projeto

Se precisar recriar o arquivo RAR, siga os passos abaixo:

1. Certifique-se de que todos os arquivos estão na pasta `sistema_clinicas`.
2. Instale o utilitário `rar`:
   ```bash
   sudo apt install rar -y
   ```
3. Compacte a pasta:
   ```bash
   rar a sistema_clinicas_django.rar sistema_clinicas
   ```

## Testando o Sistema

- **Acesse o sistema**: Após iniciar o servidor, abra `http://localhost:8000/` no navegador.
- **Login**: Use as credenciais de teste, como `admin` (senha: `lizard1240king`), para acessar todas as funcionalidades.
- **Funcionalidades**:
  - Navegue pelas seções de usuários, clínicas, pacientes, agendamentos, atendimentos e documentos.
  - Teste a busca de pacientes por nome, CPF ou telefone.
  - Faça upload de documentos e verifique a prevenção de duplicatas.
  - Consulte os logs em `logs/audit.log` para auditoria.

## Contribuições e Suporte

Para reportar problemas ou solicitar melhorias, entre em contato com o desenvolvedor ou crie um issue no repositório (se aplicável). Forneça detalhes do erro, como mensagens de log ou capturas de tela, para facilitar o suporte.
































































# Sistema de Clínicas

Sistema de gerenciamento de clínicas desenvolvido em Django, com suporte a autenticação, gestão de usuários, clínicas, pacientes, agendamentos, atendimentos e documentos.

## Requisitos
- Debian Linux (testado no Debian 11/12)
- Python 3.8+
- PostgreSQL 13+
- pip




Passos para Compactar no Debian Linux
1. Instalar o utilitário RAR:
No Debian, instale o pacote rar :
2. Criar a Estrutura do Projeto:
Crie a pasta sistema_clinicas e adicione todos os arquivos listados na estrutura acima
(conforme fornecidos na resposta anterior).
Certifique-se de que as pastas uploads/01 , uploads/02 , e logs estejam criadas:
3. Compactar em RAR:
Navegue até o diretório pai da pasta sistema_clinicas :
Compacte a pasta sistema_clinicas em um arquivo RAR:
Isso criará um arquivo sistema_clinicas_django.rar contendo todos os arquivos do
projeto.
Arquivo RAR do Projeto
sistema_clinicas_django.rar
x-rar-compressed
•
README.md Atualizado
bash
sudo apt update
sudo apt install rar -y
bash
mkdir -p sistema_clinicas/uploads/01 sistema_clinicas/uploads/02
sistema_clinicas/logs
bash
cd caminho/para/o/diretório
bash
rar a sistema_clinicas_django.rar sistema_clinicas
markdown
2. Instale dependências do sistema:
3. Configure o PostgreSQL:
Inicie o serviço:
Crie o banco de dados e usuário:
4. Descompacte o projeto:
Descompacte o arquivo RAR:
# Sistema de Clínicas
Sistema de gerenciamento de clínicas desenvolvido em Django, com suporte a
autenticação, gestão de usuários, clínicas, pacientes, agendamentos, atendimentos e
documentos.
## Requisitos
- Debian Linux (testado no Debian 11/12)
- Python 3.8+
- PostgreSQL 13+
- pip
- rar (para descompactação do arquivo RAR)
## Instalação no Debian Linux
1. **Atualize o sistema**:
```bash
sudo apt update && sudo apt upgrade -y
bash
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib
rar -y
bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
bash
sudo -u postgres psql -c "CREATE DATABASE sistema_clinicas;"
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sistema_clinicas
TO postgres;"
5. Crie e ative um ambiente virtual:
6. Instale as dependências:
7. Crie diretórios para uploads e logs:
8. Aplique as migrações:
9. Popule o banco com dados de teste:
10. Crie um superusuário:
11. Coletar arquivos estáticos:
bash
unrar x sistema_clinicas_django.rar
cd sistema_clinicas
bash
python3 -m venv venv
source venv/bin/activate
bash
pip install -r requirements.txt
bash
mkdir -p uploads/01 uploads/02 logs
chmod -R 775 uploads logs
bash
python manage.py makemigrations
python manage.py migrate
bash
python clinica/populate_db.py
bash
python manage.py createsuperuser
bash
12. Inicie o servidor:
Acesse em: http://localhost:8000/
Admin em: http://localhost:8000/admin/
Funcionalidades
Autenticação: Login com RGM/CPF e senha, com permissões por perfil (Atendente, Aluno,
Professor, Coordenador).
Gestão de Usuários: CRUD para usuários, restrito a coordenadores.
Gestão de Clínicas: Cadastro e listagem de clínicas.
Gestão de Pacientes: Cadastro unificado, busca por nome/CPF/telefone, suporte a
responsáveis legais.
Agendamentos: Agendamento com médicos e alunos, com status.
Atendimentos: Gestão com obrigatoriedade de professor monitor para alunos.
Documentos: Upload com organização em pastas, verificação de duplicatas por hash SHA-
256, logs de auditoria.
Interface: Responsiva com Bootstrap 5.3.
Dados de Teste
Usuários:
admin (COORDENADOR, RGM: RGM0001, senha: lizard1240king)
professor1 (PROFESSOR, RGM: RGM0002, senha: senha123)
aluno1 (ALUNO, RGM: RGM0003, senha: senha123)
atendente1 (ATENDENTE, RGM: RGM0004, senha: senha123)
Clínicas: Clínica Central, Clínica Norte
Pacientes: Ana Silva, João Santos (com responsável legal)
Agendamentos: 2 agendamentos
Atendimentos: 1 atendimento iniciado
Pastas: Documentos Gerais, Exames
Notas
Logs de auditoria em logs/audit.log .
python manage.py collectstatic
bash
python manage.py runserver 0.0.0.0:8000
Arquivos de upload em uploads/YYYY/MM/DD/ .
=======
# sistema
>>>>>>> 3d40e5ff04b0e30c3ff58f05fa9b202a900631d8
