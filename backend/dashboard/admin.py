from django.contrib import admin
from documents.models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'dossier', 'fichier', 'date_upload')
    list_filter = ('dossier', 'date_upload')

