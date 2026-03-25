from django.db import models
from dossiers.models import Dossier

class Intervention(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre