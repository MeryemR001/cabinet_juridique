from django.db import models
from dossiers.models import Dossier

class Document(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='documents/')
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"