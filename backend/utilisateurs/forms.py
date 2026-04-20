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

    assistante = forms.ModelChoiceField(
        queryset=User.objects.filter(role='assistante'),
        required=False,
        empty_label="Choisir une assistante"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'role'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ================= UPDATE =================
from django import forms
from .models import User

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

    assistante = forms.ModelChoiceField(
        queryset=User.objects.filter(role='assistante'),
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
            'role'
        ]

    def clean(self):
     cleaned_data = super().clean()

     dossier = cleaned_data.get("dossier")
     avocat = cleaned_data.get("avocat")

    # 🔒 règle métier
     if dossier and avocat:
        if dossier.avocat_responsable != avocat:
            raise forms.ValidationError(
                "❌ Cet avocat n'est pas responsable de ce dossier."
            )

     return cleaned_data