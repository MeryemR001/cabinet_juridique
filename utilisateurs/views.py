from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserCreateForm, UserUpdateForm
from .models import User
from .decorators import permission_required
from .permissions import has_role
from django.contrib.auth import update_session_auth_hash

# 🔥 LOGIN PROPRE (SANS ROLE FORM)
def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect_by_role(user)
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'utilisateurs/login.html', {'form': form})


# 🔥 REDIRECTION SELON ROLE
def redirect_by_role(user):
    if has_role(user, 'admin'):
        return redirect('dashboard:admin')
    elif has_role(user, 'avocat'):
        return redirect('dashboard:avocat')
    elif has_role(user, 'assistante'):
        return redirect('dashboard:assistante')
    return redirect('utilisateurs:login')


# 🔥 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('utilisateurs:login')


# 🔥 LISTE UTILISATEURS (ADMIN)
@login_required
@permission_required('utilisateurs.list')
def liste_utilisateurs(request):
    utilisateurs = User.objects.select_related('avocat').all().order_by('role')
    return render(request, 'utilisateurs/liste.html', {'utilisateurs': utilisateurs})


# 🔥 CREER UTILISATEUR
@login_required
@permission_required('utilisateurs.create')
def creer_utilisateur(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            # Relation unique: une assistante est liée à un avocat.
            if has_role(user, 'assistante'):
                user.avocat = form.cleaned_data.get('avocat')
            else:
                user.avocat = None

            user.save()  # ✅ un seul save

            return redirect('utilisateurs:liste')

        else:
            print(form.errors)  # 🔴 pour debug

    else:
        form = UserCreateForm()

    return render(request, 'utilisateurs/creer.html', {'form': form})


# 🔥 MODIFIER UTILISATEUR
@login_required
@permission_required('utilisateurs.update')
def modifier_utilisateur(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=utilisateur)
        if form.is_valid():
            user = form.save(commit=False)

            if has_role(user, 'assistante'):
                user.avocat = form.cleaned_data.get('avocat')
            else:
                user.avocat = None

            password = form.cleaned_data.get('password1')
            if password:
                user.set_password(password)
            user.save()
            if password:
                update_session_auth_hash(request, user)
            messages.success(request, "Utilisateur modifié avec succès.")
            return redirect('utilisateurs:liste')
    else:
        form = UserUpdateForm(instance=utilisateur)
    return render(request, 'utilisateurs/creer.html', {'form': form})
# 🔥 SUPPRIMER UTILISATEUR
@login_required
@permission_required('utilisateurs.delete')
def supprimer_utilisateur(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)
    utilisateur.delete()
    messages.success(request, "Utilisateur supprimé.")
    return redirect('utilisateurs:liste')