from django.contrib import admin
from .models import Audience


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'avocat', 'tribunal', 'date_audience', 'statut')
    list_filter = ('statut',)
    search_fields = ('tribunal', 'dossier__reference')