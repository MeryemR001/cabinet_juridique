from django.db import models
from employes.models import Employe
from dossiers.models import Dossier

class Document(models.Model):
    nom = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents/')
    employe = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True)
    dossier = models.ForeignKey(Dossier, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom