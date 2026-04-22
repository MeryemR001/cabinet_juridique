from django.db import models
from utilisateurs.models import User
from dossiers.models import Dossier, Client


class Facture(models.Model):
    STATUTS = [
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]

    numero = models.CharField(max_length=50, unique=True)
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.PROTECT,
        related_name='factures'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='factures'
    )
    avocat = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'avocat'},
        related_name='factures'
    )
    statut = models.CharField(max_length=20, choices=STATUTS, default='brouillon')
    date_emission = models.DateField(auto_now_add=True)
    date_echeance = models.DateField()
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcul automatique du montant TTC
        self.montant_ttc = self.montant_ht + (self.montant_ht * self.tva / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero} — {self.client}"


class LigneFacture(models.Model):
    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name='lignes'
    )
    description = models.CharField(max_length=200)
    quantite = models.DecimalField(max_digits=5, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcul automatique du total de la ligne
        self.total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} — {self.total} MAD"