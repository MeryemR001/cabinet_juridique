from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, UserCreateForm, UserUpdateForm
from .models import User
from .decorators import role_required


# 🔥 LOGIN PROPRE (SANS ROLE FORM)
def login_view(request):
    if request.user.is_authenticated:
        return _redirect_after_login(request, request.user)

    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return _redirect_after_login(request, user)
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'utilisateurs/login.html', {
        'form': form,
        'next_url': next_url,
    })


def _redirect_after_login(request, user):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect_by_role(user)


# 🔥 REDIRECTION SELON ROLE
def redirect_by_role(user):
    if user.role == 'admin':
        return redirect('dashboard:admin')
    elif user.role == 'avocat':
        return redirect('dashboard:avocat')
    elif user.role == 'assistante':
        return redirect('dashboard:assistante')
    return redirect('utilisateurs:login')


# 🔥 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('utilisateurs:login')


# 🔥 LISTE UTILISATEURS (ADMIN)
@login_required
@role_required('admin')
def liste_utilisateurs(request):
    utilisateurs = User.objects.all().order_by('role')
    return render(request, 'utilisateurs/liste.html', {'utilisateurs': utilisateurs})


# 🔥 CREER UTILISATEUR
@login_required
@role_required('admin')
def creer_utilisateur(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # relations AVANT save
            if user.role == 'avocat':
                user.assistante = form.cleaned_data.get('assistante')

            elif user.role == 'assistante':
                user.avocat = form.cleaned_data.get('avocat')

            user.save()  # ✅ un seul save

            return redirect('utilisateurs:liste')

        else:
            print(form.errors)  # 🔴 pour debug

    else:
        form = UserCreateForm()

    return render(request, 'utilisateurs/creer.html', {'form': form})


# 🔥 MODIFIER UTILISATEUR
@login_required
@role_required('admin')
def modifier_utilisateur(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=utilisateur)

        if form.is_valid():
            user = form.save(commit=False)

            # relations
            if user.role == 'avocat':
                user.assistante = form.cleaned_data.get('assistante')
                user.avocat = None

            elif user.role == 'assistante':
                user.avocat = form.cleaned_data.get('avocat')
                user.assistante = None

            else:
                user.assistante = None
                user.avocat = None

            # ✅ mot de passe
            password = form.cleaned_data.get('password1')
            if password:
                user.set_password(password)

            user.save()

            messages.success(request, "Utilisateur modifié avec succès.")
            return redirect('utilisateurs:liste')

    else:
        form = UserUpdateForm(instance=utilisateur)

    return render(request, 'utilisateurs/creer.html', {
        'form': form
    })

# 🔥 SUPPRIMER UTILISATEUR
@login_required
@role_required('admin')
def supprimer_utilisateur(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)
    utilisateur.delete()
    messages.success(request, "Utilisateur supprimé.")
    return redirect('utilisateurs:liste')