from django.contrib import admin
from .models import Audience

class AudienceAdmin(admin.ModelAdmin):
    # Remplace 'nom' par des champs existants comme client, dossier, avocat
    list_display = ('client', 'dossier', 'avocat', 'date_audience', 'statut')
    list_filter = ('statut', 'date_audience')
    search_fields = ('client__nom', 'dossier__nom', 'avocat__nom')

admin.site.register(Audience, AudienceAdmin)