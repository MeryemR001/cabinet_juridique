from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    adresse = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='clients/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"