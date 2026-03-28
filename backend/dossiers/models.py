from django.db import models
from clients.models import Client
from avocats.models import Avocat  # <- Assure-toi que l'app 'avocats' est installée dans INSTALLED_APPS

class Dossier(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom du dossier")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client associé")
    avocat = models.ForeignKey(Avocat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Avocat assigné")
    date_creation = models.DateField(auto_now_add=True, verbose_name="Date de création")
    statut = models.CharField(
        max_length=100, 
        choices=[('En cours', 'En cours'), ('Clôturé', 'Clôturé')], 
        default='En cours',
        verbose_name="Statut"
    )

    def __str__(self):
        return f"{self.nom} - {self.client.nom} - {self.avocat.nom if self.avocat else 'Sans avocat'}"