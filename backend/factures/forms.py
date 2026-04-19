from django import forms
from .models import Facture, LigneFacture


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = [
            'numero', 'dossier', 'client', 'avocat',
            'statut', 'date_echeance', 'montant_ht', 'tva', 'notes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'FAC-2024-001'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
            'montant_ht': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'tva': forms.NumberInput(attrs={'placeholder': '20.00'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Notes...', 'rows': 3}),
            'statut': forms.Select(),
            'dossier': forms.Select(),
            'client': forms.Select(),
            'avocat': forms.Select(),
        }


class LigneFactureForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ['description', 'quantite', 'prix_unitaire']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Ex: Consultation juridique'}),
            'quantite': forms.NumberInput(attrs={'placeholder': '1'}),
            'prix_unitaire': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }


# FormSet pour gérer plusieurs lignes en même temps
LigneFactureFormSet = forms.inlineformset_factory(
    Facture,
    LigneFacture,
    form=LigneFactureForm,
    extra=3,
    can_delete=True
)