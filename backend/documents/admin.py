from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_document', 'dossier', 'uploade_par', 'date_upload')
    list_filter = ('type_document',)
    search_fields = ('titre',)