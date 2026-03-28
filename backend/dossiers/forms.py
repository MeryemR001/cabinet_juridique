from django import forms
from .models import Dossier
from avocats.models import Avocat

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['nom', 'client', 'avocat', 'statut']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'avocat': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }