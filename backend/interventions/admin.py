from django.contrib import admin
from .models import Intervention

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'dossier')
    list_filter = ('date', 'dossier')
    search_fields = ('titre', 'description')