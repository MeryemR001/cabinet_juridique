from django.db import models
from clients.models import Client

class Facture(models.Model):
    numero = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.numero