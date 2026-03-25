from django.contrib import admin
from .models import Facture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'montant', 'date')
    list_filter = ('date', 'client')
    search_fields = ('numero',)
    ordering = ('-date',)