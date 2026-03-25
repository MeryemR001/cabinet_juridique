from django.contrib import admin
from .models import Dossier

@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'client', 'date_creation', 'statut')
    list_filter = ('statut', 'date_creation')
    search_fields = ('nom', 'client__nom')