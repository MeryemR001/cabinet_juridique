from django.db import models
from utilisateurs.models import User
from dossiers.models import Dossier


class Document(models.Model):
    TYPES = [
        ('acte', 'Acte'),
        ('jugement', 'Jugement'),
        ('contrat', 'Contrat'),
        ('courrier', 'Courrier'),
        ('autre', 'Autre'),
    ]

    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    titre = models.CharField(max_length=200)
    type_document = models.CharField(max_length=20, choices=TYPES, default='autre')
    fichier = models.FileField(upload_to='documents/%Y/%m/')
    uploade_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_uploades'
    )
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} — {self.dossier}"