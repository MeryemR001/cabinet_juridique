from django.db import models
from clients.models import Client  # On relie chaque dossier à un client

class Dossier(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom du dossier")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client associé")
    date_creation = models.DateField(auto_now_add=True, verbose_name="Date de création")
    statut = models.CharField(
        max_length=100, 
        choices=[('En cours', 'En cours'), ('Clôturé', 'Clôturé')], 
        default='En cours',
        verbose_name="Statut"
    )

    def __str__(self):
        return f"{self.nom} - {self.client.nom}"