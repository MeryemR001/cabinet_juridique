from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['dossier', 'titre', 'type_document', 'fichier']
        widgets = {
            'dossier': forms.Select(),
            'titre': forms.TextInput(attrs={'placeholder': 'Titre du document'}),
            'type_document': forms.Select(),
            'fichier': forms.ClearableFileInput(),
        }