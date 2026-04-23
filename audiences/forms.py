from django import forms
from .models import Audience
from utilisateurs.models import User
from utilisateurs.permissions import has_role
from dossiers.models import Dossier


class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        labels = {
            'decision': 'Décision',
        }
        fields = [
            'dossier', 'avocat', 'date_audience',
            'tribunal', 'statut', 'decision', 'observations', 'resultat'
        ]
        widgets = {
            'dossier': forms.Select(),
            'avocat': forms.Select(),
            'date_audience': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'tribunal': forms.TextInput(attrs={'placeholder': 'Ex: Tribunal de Commerce Casablanca'}),
            'statut': forms.Select(),
            'decision': forms.Select(),
            'observations': forms.Textarea(attrs={'placeholder': 'Observations...', 'rows': 3}),
            'resultat': forms.Textarea(attrs={'placeholder': 'Résultat de l audience...', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # On peut passer l'avocat connecté pour filtrer
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Seulement les avocats dans le select
        self.fields['avocat'].queryset = User.objects.filter(role='avocat')
        # Si c'est un avocat connecté → on préselectionne son nom
        if self.user and has_role(self.user, 'avocat'):
            self.fields['avocat'].initial = self.user
            self.fields['avocat'].queryset = User.objects.filter(pk=self.user.pk)
            # Seulement ses dossiers
            self.fields['dossier'].queryset = Dossier.objects.filter(
                avocat_responsable=self.user
            )

    def clean(self):
        cleaned_data = super().clean()
        statut = cleaned_data.get('statut')
        decision = cleaned_data.get('decision')

        if statut == 'tenue' and not decision:
            self.add_error('decision', 'Choisissez gagnée ou perdue.')
        if statut != 'tenue':
            cleaned_data['decision'] = ''

        return cleaned_data