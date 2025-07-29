from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clinica.models import Clinica

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        # Criar uma clínica, se não existir
        clinica, created = Clinica.objects.get_or_create(
            nome='Clínica Central',
            defaults={'endereco': 'Rua Exemplo, 123'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Criada Clínica: Clínica Central'))
        else:
            self.stdout.write(self.style.WARNING('Clínica Central já existe'))

        # Criar um superusuário, se não existir
        username = 'admin'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password='lizard1240king',
                email='admin@example.com',
                perfil='CO',
                clinica=clinica
            )
            self.stdout.write(self.style.SUCCESS(f'Criado superusuário: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superusuário {username} já existe'))

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso.'))
