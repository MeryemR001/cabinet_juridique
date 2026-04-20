from django import forms
from django.forms.widgets import Select
from dossiers.models import Dossier
from utilisateurs.models import User
from .models import Facture, LigneFacture


# ===================== DOSSIER SELECT =====================
class DossierSelect(Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # optimisation (évite requête inutile en boucle)
        self.dossiers = {
            str(d.pk): d.client_id
            for d in Dossier.objects.all().only('id', 'client_id')
        }

    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index, **kwargs)

        if value:
            client_id = self.dossiers.get(str(value))
            if client_id:
                option['attrs']['data-client'] = client_id

        return option


# ===================== FACTURE FORM =====================
class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = [
            'numero',
            'dossier',
            'client',
            'avocat',
            'statut',
            'date_echeance',
            'montant_ht',
            'tva',
            'notes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'FAC-2024-001'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
            'montant_ht': forms.NumberInput(),
            'tva': forms.NumberInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'statut': forms.Select(),
            'dossier': DossierSelect(),
            'client': forms.Select(),
            'avocat': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()

        dossier = cleaned_data.get('dossier')
        client = cleaned_data.get('client')
        avocat = cleaned_data.get('avocat')

        # ===================== 1. CLIENT ↔ DOSSIER =====================
        if dossier and client:
            if dossier.client_id != client.id:
                raise forms.ValidationError(
                    "❌ Ce dossier n'appartient pas à ce client."
                )

        # ===================== 2. AVOCAT ↔ DOSSIER (IMPORTANT) =====================
        if dossier and avocat:
            if dossier.avocat_responsable_id != avocat.id:
                raise forms.ValidationError(
                    "❌ Cet avocat n'est pas responsable de ce dossier."
                )

        # ===================== 3. SI DOSSIER EXISTE, CLIENT/AVOCAT DOIVENT MATCH =====================
        if dossier:
            if client and dossier.client_id != client.id:
                raise forms.ValidationError("Client invalide pour ce dossier.")

            if avocat and dossier.avocat_responsable_id != avocat.id:
                raise forms.ValidationError("Avocat invalide pour ce dossier.")

        return cleaned_data


# ===================== LIGNE FACTURE =====================
class LigneFactureForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ['description', 'quantite', 'prix_unitaire']
        widgets = {
            'description': forms.TextInput(),
            'quantite': forms.NumberInput(),
            'prix_unitaire': forms.NumberInput(),
        }


LigneFactureFormSet = forms.inlineformset_factory(
    Facture,
    LigneFacture,
    form=LigneFactureForm,
    extra=3,
    can_delete=True
)