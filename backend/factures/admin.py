from django.contrib import admin
from .models import Facture, LigneFacture


class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'avocat', 'statut', 'montant_ttc', 'date_emission')
    list_filter = ('statut',)
    search_fields = ('numero',)
    inlines = [LigneFactureInline]


@admin.register(LigneFacture)
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ('facture', 'description', 'quantite', 'prix_unitaire', 'total')