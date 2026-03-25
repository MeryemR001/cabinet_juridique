from django.db import models
from clients.models import Client

class RendezVous(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    motif = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.client} - {self.date}"