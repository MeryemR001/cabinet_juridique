from django.shortcuts import render, redirect, get_object_or_404
from .models import Dossier
from .forms import DossierForm

# Liste des dossiers
def liste_dossiers(request):
    dossiers = Dossier.objects.all()
    return render(request, 'dossiers/liste.html', {'dossiers': dossiers})

# Ajouter un dossier
def ajouter_dossier(request):
    if request.method == "POST":
        form = DossierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_dossiers')
    else:
        form = DossierForm()
    return render(request, 'dossiers/ajouter.html', {'form': form})

# Modifier un dossier
def modifier_dossier(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == "POST":
        form = DossierForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            return redirect('liste_dossiers')
    else:
        form = DossierForm(instance=dossier)
    return render(request, 'dossiers/modifier.html', {'form': form, 'dossier': dossier})

# Supprimer un dossier
def supprimer_dossier(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    dossier.delete()
    return redirect('liste_dossiers')