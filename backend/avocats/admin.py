from django.contrib import admin
from .models import Avocat, Assistante

@admin.register(Avocat)
class AvocatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone')
    search_fields = ('nom', 'prenom', 'email')


@admin.register(Assistante)
class AssistanteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'avocat')
    search_fields = ('nom', 'prenom', 'email')
    list_filter = ('avocat',)