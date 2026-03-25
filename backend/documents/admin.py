from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'employe', 'dossier', 'date_creation')
    list_filter = ('employe', 'dossier', 'date_creation')
    search_fields = ('nom',)