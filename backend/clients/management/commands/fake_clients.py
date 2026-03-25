from django.core.management.base import BaseCommand
from faker import Faker
from clients.models import Client

class Command(BaseCommand):
    help = 'Generate fake clients'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):  # créer 10 clients
            Client.objects.create(
                nom=fake.last_name(),
                prenom=fake.first_name(),
                email=fake.email(),
                telephone=fake.phone_number(),
                adresse=fake.address()
            )
        self.stdout.write(self.style.SUCCESS('Clients ajoutés avec succès!'))