from django.db import models
from clients.models import Client
from dossiers.models import Dossier
from avocats.models import Avocat

class Audience(models.Model):
    STATUT_CHOICES = [
        ('Prévue', 'Prévue'),
        ('Clôturée', 'Clôturée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, verbose_name="Dossier")
    avocat = models.ForeignKey(Avocat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Avocat")
    date_audience = models.DateField(verbose_name="Date de l'audience")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Prévue', verbose_name="Statut")

    def __str__(self):
        return f"{self.client.nom} - {self.dossier.nom} - {self.date_audience} - {self.statut}"