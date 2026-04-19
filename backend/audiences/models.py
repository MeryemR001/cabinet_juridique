from django.db import models
from utilisateurs.models import User
from dossiers.models import Dossier


class Audience(models.Model):
    STATUTS = [
        ('programmee', 'Programmée'),
        ('tenue', 'Tenue'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée'),
    ]

    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='audiences'
    )
    avocat = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'avocat'},
        related_name='audiences'
    )
    date_audience = models.DateTimeField()
    tribunal = models.CharField(max_length=200)
    statut = models.CharField(max_length=20, choices=STATUTS, default='programmee')
    observations = models.TextField(blank=True)
    resultat = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audience {self.dossier} — {self.date_audience}"