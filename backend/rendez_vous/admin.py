from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'heure', 'motif')
    list_filter = ('date',)
    search_fields = ('motif',)
    ordering = ('-date',)