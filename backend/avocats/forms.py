from django import forms
from .models import Avocat, Assistante

class AvocatForm(forms.ModelForm):
    class Meta:
        model = Avocat
        fields = ['nom', 'prenom', 'email', 'telephone']


class AssistanteForm(forms.ModelForm):
    class Meta:
        model = Assistante
        fields = ['nom', 'prenom', 'email', 'telephone', 'avocat']