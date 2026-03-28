from django.db import models

class Avocat(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Assistante(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    avocat = models.ForeignKey(Avocat, on_delete=models.CASCADE, related_name="assistantes")

    def __str__(self):
        return f"{self.nom} {self.prenom}"