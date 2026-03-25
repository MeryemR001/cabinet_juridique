from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'fichier', 'employe', 'dossier']  # utiliser les vrais noms de champs