from django.contrib import admin
from .models import Audience

@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'heure', 'lieu', 'dossier')
    list_filter = ('date', 'lieu')
    search_fields = ('titre', 'lieu')
    ordering = ('-date',)