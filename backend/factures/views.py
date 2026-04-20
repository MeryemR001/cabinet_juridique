from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from utilisateurs.decorators import role_required
from .models import Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet
from dossiers.models import Dossier

@login_required
@role_required('admin', 'avocat')
@login_required
@role_required('admin', 'avocat')
def liste_factures(request):
    if request.user.role == 'avocat':
        factures = Facture.objects.filter(avocat=request.user).exclude(statut='annulee')
    else:
        factures = Facture.objects.exclude(statut='annulee')

    factures_envoyees_count = factures.filter(statut='envoyee').count()
    chiffre_affaires = factures.filter(statut='payee').aggregate(
        total=Sum('montant_ttc')
    )['total'] or 0

    return render(request, 'factures/liste.html', {
        'factures': factures,
        'factures_envoyees_count': factures_envoyees_count,
        'chiffre_affaires': chiffre_affaires,
    })

@login_required
@role_required('admin', 'avocat')
def detail_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    lignes = facture.lignes.all()
    return render(request, 'factures/detail.html', {
        'facture': facture,
        'lignes': lignes,
    })

@login_required
@role_required('admin', 'avocat')
def creer_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        formset = LigneFactureFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            facture = form.save()
            formset.instance = facture
            formset.save()
            facture.save()
            return redirect('factures:liste')
    else:
        form = FactureForm()
        formset = LigneFactureFormSet()
    return render(request, 'factures/creer.html', {
        'form': form,
        'formset': formset,
        'dossiers_avocats': Dossier.objects.all().only('id', 'avocat_responsable_id'),
    })

@login_required
@role_required('admin', 'avocat')
def modifier_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        formset = LigneFactureFormSet(request.POST, instance=facture)
        if form.is_valid() and formset.is_valid():
            facture = form.save()
            formset.save()
            facture.save()
            return redirect('factures:liste')
        else:
            print(f"Erreurs form: {form.errors}")
            print(f"Erreurs formset: {formset.errors}")
    else:
        form = FactureForm(instance=facture)
        formset = LigneFactureFormSet(instance=facture)
    return render(request, 'factures/creer.html', {
        'form': form,
        'formset': formset,
        'facture': facture,
        'dossiers_avocats': Dossier.objects.all().only('id', 'avocat_responsable_id'),
    })

@login_required
@role_required('admin')
def supprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    facture.delete()
    return redirect('factures:liste')

@login_required
@role_required('admin', 'avocat')
def imprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    lignes = facture.lignes.all()
    return render(request, 'factures/imprimer.html', {
        'facture': facture,
        'lignes': lignes,
    })