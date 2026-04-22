from django.db import models
from utilisateurs.models import User


class Client(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    cin = models.CharField(max_length=20, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Dossier(models.Model):
    STATUTS = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('clos', 'Clos'),
    ]

    reference = models.CharField(max_length=50, unique=True)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='dossiers'
    )
    
    avocat_responsable = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={'role': 'avocat'},
        related_name='dossiers'
    )
    statut = models.CharField(max_length=20, choices=STATUTS, default='ouvert')
    date_ouverture = models.DateField(auto_now_add=True)
    date_cloture = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.reference} — {self.titre}"


class Intervention(models.Model):
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='interventions'
    )
    avocat = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'avocat'},
        related_name='interventions'
    )
    description = models.TextField()
    heures_travaillees = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intervention de {self.avocat} sur {self.dossier}"