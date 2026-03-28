from django import forms
from .models import Audience
from dossiers.models import Dossier
from avocats.models import Avocat

class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ['client', 'dossier', 'avocat', 'date_audience', 'statut']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control', 'id': 'client-select'}),
            'dossier': forms.Select(attrs={'class': 'form-control', 'id': 'dossier-select'}),
            'avocat': forms.Select(attrs={'class': 'form-control'}),
            'date_audience': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        dossier = cleaned_data.get('dossier')
        avocat = cleaned_data.get('avocat')

        # Vérifie que le dossier appartient bien au client
        if dossier and client and dossier.client != client:
            self.add_error('dossier', 'Ce dossier n’appartient pas au client sélectionné.')

        # Vérifie que l’avocat est bien assigné au dossier
        if dossier and avocat:
            if dossier.avocat != avocat:
                self.add_error('avocat', 'Cet avocat n’est pas assigné au dossier sélectionné.')

        return cleaned_data