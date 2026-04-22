from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# ================= CREATE =================
class UserCreateForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('admin', 'Admin'),
            ('avocat', 'Avocat'),
            ('assistante', 'Assistante'),
        ],
        required=True
    )

    avocat = forms.ModelChoiceField(
        queryset=User.objects.filter(role='avocat'),
        required=False,
        empty_label="Choisir un avocat"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'role',
            'profile_picture',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        avocat = cleaned_data.get('avocat')

        if role == 'assistante' and not avocat:
            self.add_error('avocat', "Veuillez sélectionner un avocat pour l'assistante.")

        if role != 'assistante':
            cleaned_data['avocat'] = None

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        required=False
    )

    password2 = forms.CharField(
        label="Confirmer mot de passe",
        widget=forms.PasswordInput,
        required=False
    )

    avocat = forms.ModelChoiceField(
        queryset=User.objects.filter(role='avocat'),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'role',
            'profile_picture',
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        avocat = cleaned_data.get('avocat')

        if role == 'assistante' and not avocat:
            self.add_error('avocat', "Veuillez sélectionner un avocat pour l'assistante.")

        if role != 'assistante':
            cleaned_data['avocat'] = None

        return cleaned_data