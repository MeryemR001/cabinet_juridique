from django import forms
from .models import Client, Dossier, Intervention
from utilisateurs.models import User


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'telephone', 'email', 'adresse', 'cin']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'adresse': forms.Textarea(attrs={'placeholder': 'Adresse', 'rows': 3}),
            'cin': forms.TextInput(attrs={'placeholder': 'CIN'}),
        }


class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['reference', 'titre', 'description', 'client', 'avocat_responsable', 'statut']
        widgets = {
            'reference': forms.TextInput(attrs={'placeholder': 'DOS-2024-001'}),
            'titre': forms.TextInput(attrs={'placeholder': 'Titre du dossier'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 3}),
            'client': forms.Select(),
            'avocat_responsable': forms.Select(),
            'statut': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Seulement les avocats dans le select
        self.fields['avocat_responsable'].queryset = User.objects.filter(role='avocat')


class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['dossier', 'description', 'heures_travaillees']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Description de l intervention', 'rows': 3}),
            'heures_travaillees': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }

    def __init__(self, *args, **kwargs):
        # On passe l'avocat connecté depuis la vue
        self.avocat = kwargs.pop('avocat', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.avocat:
            instance.avocat = self.avocat
        if commit:
            instance.save()
        return instance