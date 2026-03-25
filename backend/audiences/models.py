from django.db import models
from dossiers.models import Dossier

class Audience(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateField()
    heure = models.TimeField()
    lieu = models.CharField(max_length=200)
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre