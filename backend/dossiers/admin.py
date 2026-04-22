from django.contrib import admin
from .models import Client, Dossier, Intervention


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'email', 'date_creation')
    search_fields = ('nom', 'prenom', 'cin')


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ('reference', 'titre', 'client', 'avocat_responsable', 'statut', 'date_ouverture')
    list_filter = ('statut',)
    search_fields = ('reference', 'titre')


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'avocat', 'heures_travaillees', 'date')